import os
import logging
from sqlite3 import IntegrityError
import requests


from model import Thing
from categories import get as Categories


log = logging.getLogger('root')
class Thingiverse:
    auth_token = "56edfc79ecf25922b98202dd79a291aa"
    s = requests.Session()

    def __init__(self, username: str) -> None:
        self.s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0"
        self.s.headers["Authorization"] =  f"Bearer {self.auth_token}"
        self.username = username

    def get_models(self) -> None:
        page = 1
        per_page = 20

        while True:
            url = f"https://api.thingiverse.com/users/{self.username}/search/?page={page}&per_page={per_page}&type=things&sort=newest"
            r = self.s.get(url)
            if r.status_code != 200:
                log.error(f"Get \"{self.username}\" models {r.status_code}: {r.text}")
                break

            data = r.json()
            total = data['total']
            for things in data['hits']: 
                category = self.s.get(f"https://api.thingiverse.com/things/{things['id']}/categories").json()[0]['name']
                model_info = {
                    "id": things['id'],
                    "title": things['name'],
                    "owner": self.username,
                    "category_id": Categories(category),
                    "image": things['thumbnail'],
                }
                Thing.insert(**model_info).on_conflict_ignore().execute()

            if page * per_page >= total:
                break
            page += 1
        return 

    def download(self, id: int):
        thing = Thing.get_by_id(id)
        r = self.s.get(thing.image)
        if r.status_code != 200:
            return None
        if not os.path.isdir('models'):
            os.mkdir('models')
        open(f"models/{thing.id}.jpg", 'wb').write(r.content)
        result = {
            "image": f"models/{thing.id}.jpg",
            "files": set()
        }
        files_url = f'https://api.thingiverse.com/things/{thing.id}/files'
        r = self.s.get(files_url)
        if r.status_code != 200:
            return None
        for file in r.json():
            if not file['name'].endswith(".stl"):
                continue
            c = self.s.get(file['url'])
            if c.status_code != 200:
                continue
            open(f"models/{file['name']}", 'wb').write(c.content)
            result['files'].add(f"models/{file['name']}")
        return result

if __name__ == '__main__':
    Thing.create_table()
    api = Thingiverse("drewmoseley")
    api.get_models()
    things = Thing.select().where((Thing.owner == "drewmoseley") & (Thing.status == 0))
    api.download(things[0].id)
    pass