import csv

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