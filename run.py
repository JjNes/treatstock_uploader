import csv
import logger
import os
import zipfile
import shutil
import time


log = logger.setup_custom_logger('root')


from treatstock import Treatstock, Thing
from thingiverse import Thingiverse
import categories as categories


def save_task(items):
    with open('task.csv', 'w', newline='') as csvfile:
        fieldnames = ["username" ,"login", "password", "delay_min", "status"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in items:
            writer.writerow(item)

def save_model(file_path, items):
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ["name", "categories","path", "status"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in items:
            writer.writerow(item)

def download(task):
    res = Thingiverse(task['username']).download(3)
    log.info(f"Downloaded {res} models of {task['username']}")
    task['status'] = 'downloaded'
    save_task(tasks)

try:
    tasks = []

    # Load tasks
    with open('task.csv', 'r', newline='') as csvfile:
        task = csv.DictReader(csvfile, delimiter=',')
        for row in task:
            tasks.append(row)
        log.info(f"Load {len(tasks)} tasks")

    for task in tasks:
        if task['status'] == '':
            download(task)

        if task['status'] == 'downloaded':
            mm = []
            model_file_path = f"models/{task['username']}.csv"
            try:
                with open(model_file_path, 'r', newline='') as csvfile:
                    ss = csv.DictReader(csvfile, delimiter=',')
                    for row in ss:
                        mm.append(row)
            except FileNotFoundError:
                log.error(f"Models for user {task['username']} not downloaded")
                download(task)

            api = Treatstock()

            for m in mm:
                if m['status'] == 'True':
                    log.info(f"{m['name']} is already upload")
                    continue

                if not api.is_login():
                    is_login = api.login(task['login'], task['password'])
                    if is_login:
                        log.info(f"Login {task['login']} OK")
                    else:
                        log.error(f"Login {task['login']} FALSE")
                        break
                    
                # Extract
                with zipfile.ZipFile(m['path'], 'r') as archive:
                    archive.extractall(m['path'].strip(".zip"))
                # Find model's files
                ext =  [".stl", ".ply", ".obj", ".3mf", ".jpeg", ".png", ".gif", ".jpg"]
                result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(m['path'].strip(".zip")) for f in filenames if os.path.splitext(f)[1].lower() in ext]
                model = Thing(m['name'], f"3D model of {m['name']}")
                model.set_category(categories.get(m['categories']))
                model.set_files(result)
                if model.bad:
                    shutil.rmtree(m['path'].strip(".zip"))
                    save_model(model_file_path, mm) 
                    continue
                # Upload
                id = api.create_from_model(model)
                model.id = id
                if id:
                    log.info(f"Model {m['name']} is uploaded") 
                    is_upload = api.publish(model.publish())
                    if not is_upload:
                        log.error(f"Model {m['name']} NOT published")  
                    else:
                        log.info(f"Model {m['name']} is published")         
                        m['status'] = True
                else:
                    log.error(f"Model {m['name']} NOT uploaded")
                shutil.rmtree(m['path'].strip(".zip"))
                save_model(model_file_path, mm)   
                time.sleep(int(task['delay_min']) * 60)
except Exception as e:
    log.error(e)
