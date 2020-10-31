from models.base_model import BaseModel
import peewee as pw
from models.user import User
from models.image import Image




class Donation(BaseModel):
    amount=pw.IntegerField()
    donor=pw.ForeignKeyField(User , backref="mydonations")
    image=pw.ForeignKeyField(Image, backref="donationdetail")