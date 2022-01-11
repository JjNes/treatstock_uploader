from enum import Enum

import treatstock.exception as exception

from PIL import Image

class Currency(Enum):
    USD = "USD"


class Thing():
    id = None
    files = []

    def __init__(self, title, description, price_value = 0.00, price_currency = Currency.USD) -> None:
        self.title = title
        self.category_id = 4462 #All things
        self.description = description
        self.price_value = price_value
        self.price_currency = price_currency.value

    def set_files(self, files) -> None:
        for f in files:
            if f.endswith(".png"):
                img = Image.open(f).convert('L')
                pix = img.load()
                if pix[0, 0] != pix[0, 1]:
                    continue
            self.files.append(f)
                    


    def to_dict(self) -> dict:
        if not id:
            raise exception.ModelNotCreated
        return {
            "Model3dEditForm": {
                "description": self.description,
                "title": self.title,
                "id": self.id,
                "pricePerPrint": self.price_value,
                "priceCurrency": self.price_currency,
                "submitForm":1,
                "categoryId": self.category_id,
                "submitMode": "publish"
            }
        }

    def set_category(self, id: int = None) -> None:
        if id:
            self.category_id = id
    
    def publish(self) -> dict:
        return self.to_dict()
    