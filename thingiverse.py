import os
import re
import json
import time
import zipfile
import requests
import pickle


class Thingiverse:
    auth_token = "56edfc79ecf25922b98202dd79a291aa"
    s = requests.Session()
    root_dir = "models"

    def __init__(self, username: str) -> None:
        self.s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0"
        self.s.headers["Authorization"] =  f"Bearer {self.auth_token}"
        self.username = username
        self.output = "/".join([self.root_dir, self.username])
        try:
            os.makedirs(self.output)      
        except:
            pass

    def download(self, delay: int = 0) -> bool:
        url = f"https://api.thingiverse.com/users/{self.username}/search/?page=1&per_page=40&type=things&sort=newest"
        r = self.s.get(url)
        if r.status_code != 200:
            return False
        data = r.json()
        files = []
        for things in data['hits']:        
            public_url = things['public_url']
            model_name = things['name']
            zip = self.s.get(public_url+"/zip")
            if zip.status_code != 200:
                continue
            file_name = zip.url[zip.url.rfind("/")+1:]
            file_path = "/".join([self.output, file_name])
            open(file_path, 'wb').write(zip.content)
            archive = zipfile.ZipFile(file_path, 'r')
            archive.extractall(file_path.strip(".zip"))
            archive.close()
            os.remove(file_path)
            file = {"title": model_name, "path": file_path.strip(".zip")}
            files.append(file)
            time.sleep(delay)
        pickle.dump(files, open("/".join([self.output, "models.dat"]), 'wb'))
        return True