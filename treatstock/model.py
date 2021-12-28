from enum import Enum

import exception


class Currency(Enum):
    USD = "USD"


class Thing():
    id = None
    files = []

    def __init__(self, title, description, price_value = 0.00, price_currency = Currency.USD) -> None:
        self.title = title
        self.description = description
        self.price_value = price_value
        self.price_currency = price_currency

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

    def add_file(self, name, path) -> None:
        self.files.append({"name": name, "path": path})
    