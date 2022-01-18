from peewee import *

db = SqliteDatabase('models.db')


class Thing(Model):
    id = PrimaryKeyField(null=False)
    publish_id = IntegerField(null=True, default=None)
    title = CharField()
    category_id = IntegerField(default=4462)
    status = IntegerField(default=0)
    owner = CharField()

    class Meta:
        database = db

    def set_files(self, files) -> None:
        self.files = files
               
    def to_dict(self) -> dict:
        return {
            "Model3dEditForm": {
                "description": f"3D model of {self.owner}",
                "title": self.title,
                "id": self.publish_id,
                "pricePerPrint": 0.00,
                "priceCurrency": "USD",
                "submitForm":1,
                "categoryId": self.category_id,
                "submitMode": "publish"
            }
        }
    