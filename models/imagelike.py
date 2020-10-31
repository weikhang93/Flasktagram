import peewee as pw
from models.base_model import BaseModel
from models.image import Image
from models.user import User



class ImageLike(BaseModel):
    image=pw.ForeignKeyField(Image,backref="likes")
    liker=pw.ForeignKeyField(User,backref="likes")

