import csv
import logging


import logger
log = logger.setup_custom_logger('root')


from treatstock import Treatstock
from thingiverse import Thingiverse




api = Treatstock()


#r = api.create_model([])


tv = Thingiverse("PRIma")
#tv.download()


with open('task.csv', 'r', newline='') as csvfile:
    task = csv.DictReader(csvfile, delimiter=',')
    for row in task:
        res = Thingiverse(row['username']).download(10)
        print(res)        



"""
archive = zipfile.ZipFile(file_path, 'r')
                archive.extractall(file_path.strip(".zip"))
                archive.close()
                with open(file_path.strip(".zip")+"/name.txt", "wb") as t:
                    t.write(model_name.encode('utf-8'))
                os.remove(file_path)
"""