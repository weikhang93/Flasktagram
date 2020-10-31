import peewee as pw
from models.base_model import BaseModel
from models.user import User
from playhouse.hybrid import hybrid_property


class Image(BaseModel):
    user=pw.ForeignKeyField(User , backref="images")
    images_pathway=pw.CharField()


    @hybrid_property
    def full_image_url(self):
        from app import app
        
        return app.config["S3_LOCATION"]+self.images_pathway


    @hybrid_property
    def top10(self):
        from models.donation import Donation


        return Donation.select().where(Donation.image==self.id).order_by(Donation.amount.desc()).limit(10)


