import peewee as pw
from models.base_model import BaseModel
from models.image import Image
from models.user import User


class ImageComment(BaseModel):
    image=pw.ForeignKeyField(Image,backref="comments")
    commentator=pw.ForeignKeyField(User,backref="comments")
    comment=pw.TextField()