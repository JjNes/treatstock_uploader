from enum import Enum

import exception


class Currency(Enum):
    USD = "USD"


class Model:
    id = None
    is_created = False
    files = []

    def __init__(self, title, description, price_value = 0.00, price_currency = Currency.USD) -> None:
        self.title = title
        self.description = description
        self.price_value = price_value
        self.price_currency = price_currency

    def to_dict(self) -> dict:
        if not self.is_created:
            raise exception.ModelNotCreated
        return {
            "Model3dEditForm": {
                "description": self.description,
                "title": self.title,
                "id": self.id,
                "pricePerPrint": self.price_value,
                "priceCurrency": self.price_currency,
                "submitForm":1
            }
        }
    
    def edit(self) -> dict:
        return self.to_dict()

    def publish(self) -> dict:
        data = self.to_dict()
        data["submitMode"] = "publish"
        return data
    
    def unpublish(self) -> dict:
        data = self.to_dict()
        data["submitMode"] = "unpublish"
        return data      

    def add_files(self, files) -> bool:
        for file in files:
            data = open(file, 'rb')
            name = "ads"


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

        uploaded_files_uuids = []
        for f in files:
            
            result = self.__add_file(csfr, ff)
            if result:
                uploaded_files_uuids.append(result)
    