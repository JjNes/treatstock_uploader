import os
import re
import json
import requests
import pickle



class Treatstock:
    s = requests.Session()
    url = "https://www.treatstock.com"
    is_login = False

    def __init__(self) -> None:
        self.s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0"

    def __get_csfr(self, text: str, p: str = None) -> str:
        csfr_index = 0
        if p:
            csfr_index = text.find(p)
            if csfr_index == -1:
                raise Exception("Pattern not found")
        match = re.search(r'name="_frontendCSRF" value="[\w\S]+">', text[csfr_index:]) 
        if not match:
            raise Exception("CSFR not found")
        csfr = match[0].strip('name="_frontendCSRF" value="').strip('">')
        return csfr


    def login(self, login: str, password: str) -> bool:
        login_url = self.url + "/user/login"
        r = self.s.get(login_url)
        if r.status_code != 200:
            return False
        csfr = self.__get_csfr(r.text)
        data = {
            "_frontendCSRF": csfr,
            "LoginForm[redirectTo]": "",
            "LoginForm[email]": login,
            "LoginForm[password]": password,
            "LoginForm[rememberMe]": "0",
            "login-button": ""
        }
        r = self.s.post(login_url, data=data)
        if r.status_code != 200:
            return False
        self.is_login = True
        return True
    
    def __add_file(self, csfr, filedata) -> str:
        url = self.url + "/catalog/upload-model3d/add-file"
        data = {"_frontendCSRF": csfr}
        files = {"files": filedata}
        r = self.s.post(url, files=files, data=data)
        r_data = json.loads(r.json())
        if r.status_code == 200 and r_data["success"] == True:
            match = re.search(r'\w+.\w+$', filedata.name) 
            if match:
                name = match[0]
                return r_data["uuids"][name]
        return None

    def load_from_dat(self, dat_file) -> bool:
        things = pickle.load(open(dat_file, 'rb'))
        ext =  [".stl", ".ply", ".obj", ".3mf", ".jpeg", ".png", ".gif", ".jpg"]
        for thing in things:
            result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(thing["path"]) for f in filenames if os.path.splitext(f)[1].lower() in ext]
            model = self.create_model(result)
            if model:
                self.edit(model, thing["title"], "Test")
        return True
    
    def create_model(self, files) -> str:
        if not self.is_login:
            raise Exception("Not login")

        url = self.url + "/upload?noredir=1"
        r = self.s.get(url)
        if r.status_code != 200:
            return None
        csfr = self.__get_csfr(r.text, "/upload/file-upload")
        uploaded_files_uuids = []
        for f in files:
            ff = open(f, 'rb')
            result = self.__add_file(csfr, ff)
            if result:
                uploaded_files_uuids.append(result)

        data = {
            "uploadedFilesUuids": uploaded_files_uuids,
            "isPlaceOrderState": 0,
            "isWidget": 1
        }
        create_url = self.url + "/catalog/upload-model3d/create-model3d?noredir=1"
        r = self.s.post(create_url, json=data)
        if r.status_code==200 and r.json()["success"]:
            return r.json()["model3dId"] 
        return None

    def edit(self, id: int, title, description) -> bool:
        if not self.is_login:
            raise Exception("Not login")

        url = self.url + "/my/model/edit/" + str(id)
        r = self.s.get(url)
        csfr = self.__get_csfr(r.text, "/my/model/edit")
        headers = {"X-CSRF-Token": csfr}
        data = {
            "Model3dEditForm": {
                "description": description,
                "title": title,
                "id": id,
                "pricePerPrint":"0.00",
                "priceCurrency":"USD",
                "submitForm":1
            }
        }
        r = self.s.post(url, json=data, headers=headers)
        if r.status_code!= 200:
            return False
        return True