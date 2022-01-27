from peewee import *

db = SqliteDatabase('models.db')


class Thing(Model):
    id = PrimaryKeyField(null=False)
    publish_id = IntegerField(null=True, default=None)
    title = CharField()
    category_id = IntegerField(default=4462)
    status = IntegerField(default=0)
    owner = CharField()
    image = CharField()

    class Meta:
        database = db

    def set_files(self, files) -> None:
        self.files = files
               
    def to_dict(self) -> dict:
        return {
            "Model3dEditForm": {
                "categoryId": self.category_id,
                "description": f"3D model of {self.owner}\nThe models were repaired and checked for printability.",       
                "id": self.publish_id,
                "priceCurrency": "USD",
                "pricePerPrint": "0.00",   
                "submitForm":1,
                "submitMode": "publish",
                "title": self.title
            }
        }
    