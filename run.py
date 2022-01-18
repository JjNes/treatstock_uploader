import csv
import logger
import os
import zipfile
import shutil
import time

from PIL import Image

log = logger.setup_custom_logger('root')


from treatstock import Treatstock
from thingiverse import Thingiverse
from model import Thing




if __name__ == '__main__':
    Thing.create_table()


    tasks = []
    if os.path.isfile('task.csv'):
        with open('task.csv', 'r', newline='') as csvfile:
            task = csv.DictReader(csvfile, delimiter=',')
            for row in task:
                tasks.append(row)
            log.info(f"Load {len(tasks)} tasks")
    else:
        log.error("task.csv not found!")
        exit(0)

    for task in tasks:
        username = task['username']
        api_thing = Thingiverse(username)
        api_thing.get_models()
        api_thing.download()

        api_tre = Treatstock()

        models = Thing.select().where((Thing.owner == username) & (Thing.status == 200))
        for m in models:

            with zipfile.ZipFile(f"models/{m.id}", 'r') as archive:
                archive.extractall(f"models/{m.id}zip")

            # Files
            models_ext =  [".stl", ".ply", ".obj", ".3mf"]
            img_ext =  [".jpeg", ".png", ".gif", ".jpg"]

                
            files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(f"models/{m.id}zip") for f in filenames if os.path.splitext(f)[1].lower() in models_ext]
            images = [os.path.join(dp, f) for dp, dn, filenames in os.walk(f"models/{m.id}zip") for f in filenames if os.path.splitext(f)[1].lower() in img_ext]

            buf = []
            for f in images:
                img = Image.open(f).convert('L')
                pix = img.load()
                if pix[4, 4] == 200:
                    continue
                buf.append(f)
            images = buf

            if len(images) == 0:
                log.info(f"Model {m.title} is BAD")
                shutil.rmtree(f"models/{m.id}zip")
                m.status = 500
                m.save()
                continue

            result = files + images
            m.set_files(result)
            
            if not api_tre.is_login():
                api_tre.login(task['login'], task['password'])
                log.info("Login OK")
     
            id = api_tre.create_from_model(m)
            if id:
                m.publish_id = id
                log.info(f"Model {m.title} is uploaded") 
                is_upload = api_tre.publish(m.to_dict())
                if not is_upload:
                    log.error(f"Model {m.title} NOT published")  
                else:
                    log.info(f"Model {m.title} is published")         
                    m.status = 202
            else:
                log.error(f"Model {m.title} NOT uploaded")
            m.save()
            shutil.rmtree(f"models/{m.id}zip")
            time.sleep(int(task['delay_min']) * 60)
            
