import os
import time
import zipfile
import requests


class Thingiverse:
    auth_token = "56edfc79ecf25922b98202dd79a291aa"
    s = requests.Session()

    def __init__(self, username: str) -> None:
        self.s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0"
        self.s.headers["Authorization"] =  f"Bearer {self.auth_token}"
        self.username = username

    def download(self, delay: int = 0) -> bool:
        page = 1
        per_page = 20

        while True:
            url = f"https://api.thingiverse.com/users/{self.username}/search/?page={page}&per_page={per_page}&type=things&sort=newest"
            r = self.s.get(url)
            if r.status_code != 200:
                return False
            data = r.json()
            total = data['total']
            for things in data['hits']:        
                public_url = things['public_url']
                model_name = things['name']
                zip = self.s.get(public_url+"/zip")
                if zip.status_code != 200:
                    continue
                print(f"Model '{model_name}' downloaded")
                file_name = zip.url[zip.url.rfind("/")+1:]
                file_path = "/".join(["models", self.username])
                try:
                    os.makedirs(file_path)
                except OSError:
                    pass

                file_path = "/".join([file_path, file_name])
                open(file_path, 'wb').write(zip.content)
                archive = zipfile.ZipFile(file_path, 'r')
                archive.extractall(file_path.strip(".zip"))
                archive.close()
                with open(file_path.strip(".zip")+"/name.txt", "wb") as t:
                    t.write(model_name.encode('utf-8'))
                os.remove(file_path)
                time.sleep(delay)
            # Exit
            if page * per_page >= total:
                break
            page += 1
        return True