import os
import time
import logging
import requests
import math
import csv


log = logging.getLogger('root')
class Thingiverse:
    auth_token = "56edfc79ecf25922b98202dd79a291aa"
    s = requests.Session()

    def __init__(self, username: str) -> None:
        self.s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0"
        self.s.headers["Authorization"] =  f"Bearer {self.auth_token}"
        self.username = username

    def download(self, delay: int = 0) -> int:
        page = 1
        per_page = 20
        downloaded = []

        while True:
            url = f"https://api.thingiverse.com/users/{self.username}/search/?page={page}&per_page={per_page}&type=things&sort=newest"
            r = self.s.get(url)
            if r.status_code != 200:
                log.error(f"Donload models {r.status_code}: {r.text}")
                continue
            data = r.json()
            total = data['total']
            # Page info
            log.info(f"Page {page}/{math.ceil(total/per_page)}")
            for things in data['hits']:        
                public_url = things['public_url']
                model_name = things['name']

                categories = self.s.get(f"https://api.thingiverse.com/things/{things['id']}/categories").json()[0]['name']
                zip = self.s.get(public_url+"/zip")
                if zip.status_code != 200:
                    log.warning(f"Can't download zip for model '{model_name}' Code:{zip.status_code}")
                    continue
                
                file_name = zip.url[zip.url.rfind("/")+1:]
                file_path = "/".join(["models", self.username])
                try:
                    os.makedirs(file_path)
                    log.info(f"Create dir for {self.username}")
                except OSError:
                    pass
                zip_path = "/".join([file_path, file_name])
                open(zip_path, 'wb').write(zip.content)
                log.info(f"Model '{model_name}' downloaded")
                model_info = {'name': model_name, "categories": categories, 'path': zip_path, 'status': False}
                downloaded.append(model_info)
                # Save list
                with open("/".join(["models", f"{self.username}.csv"]), 'w', newline='') as csvfile:
                    fieldnames = ["name", "categories","path", "status"]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for item in downloaded:
                        try:
                            writer.writerow(item)
                        except:
                            pass
                log.info(f"Wait {delay}s")
                time.sleep(delay)
            if page * per_page >= total:
                break
            page += 1
        return len(downloaded)