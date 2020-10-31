import peewee as pw
from models.base_model import BaseModel
from models.user import User


class FanIdol(BaseModel):
    fan = pw.ForeignKeyField(User, backref="myidol")
    idol = pw.ForeignKeyField(User, backref="myfan")
    approved = pw.BooleanField(default=False)
    blocked=pw.BooleanField(default=False)

