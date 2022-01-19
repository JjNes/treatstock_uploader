import csv
import logger
import os
import time

from PIL import Image

log = logger.setup_custom_logger('root')


from treatstock import Treatstock
from thingiverse import Thingiverse
from model import Thing


if __name__ == '__main__':
    Thing.create_table()

    try:
        tasks = []
        with open('task.csv', 'r', newline='') as csvfile:
            task = csv.DictReader(csvfile, delimiter=',')
            for row in task:
                tasks.append(row)
            log.info(f"Load {len(tasks)} tasks")
    except:
        raise Exception("task.csv not found!")
        

    for task in tasks:
        username = task['username']
        api_thing = Thingiverse(username)
        log.info(f"Update list of {username} models")
        api_thing.get_models()

        api_tre = Treatstock()

        models = Thing.select().where((Thing.owner == username) & (Thing.status == 0))
        for m in models:
            files = api_thing.download(m.id)
            try:   
                if not files:
                    m.status = 404
                    raise Exception(f"Model {m.title} is NOT downloaded")
                log.info(f"Model {m.title} is downloaded")
                # Check image
                img = Image.open(files['image']).convert('L')
                pix = img.load()
                if pix[4, 4] == 200: 
                    m.status = 500
                    raise Exception(f"Model {m.title} is BAD")

                # Join file to one list
                files_to = [f for f in files['files']]
                files_to.append(files['image'])
                # Setup files to model
                m.set_files(files_to)
                # Login
                if not api_tre.is_login():
                    api_tre.login(task['login'], task['password'])
                    log.info("Login OK")
                # Upload model
                id = api_tre.create_from_model(m)
                if id:
                    m.publish_id = id
                    log.info(f"Model {m.title} is uploaded") 
                    is_upload = api_tre.publish(m.to_dict())
                    if not is_upload:
                        raise Exception(f"Model {m.title} NOT published")
                    else:
                        log.info(f"Model {m.title} is published")         
                        m.status = 202
                else:
                    raise Exception(f"Model {m.title} NOT uploaded")
            except Exception as ex:
                log.error(ex, exc_info=True)

            if files:
                os.remove(files['image'])
                for f in files['files']:
                    os.remove(f)
            m.save()
            time.sleep(int(task['delay_min']) * 60)
            
