from models.base_model import BaseModel
import peewee as pw
from flask_login import UserMixin
from playhouse.hybrid import hybrid_property







class User(BaseModel,UserMixin):
    username=pw.CharField(unique=True)
    email=pw.CharField(unique=True)
    hashed_password=pw.CharField()
    profile_image_pathway=pw.CharField(null=True, default="genius.gif")
    is_private=pw.CharField(default=False)
    



    @hybrid_property
    def full_image_path(self):
        if self.profile_image_pathway!=None:
            from app import app
            return app.config["S3_LOCATION"]+self.profile_image_pathway


    def follow(self,idol_id):
        from models.fanidol import FanIdol

        idol=User.get_by_id(int(idol_id))

        if idol.is_private=="False":
            fanidol=FanIdol(fan=self.id,idol=idol_id, approved=True)
        
        else:
            fanidol=FanIdol(fan=self.id,idol=idol_id)
            

        fanidol.save()

    def unfollow(self,idol_id):
        from models.fanidol import FanIdol

        fanidol=FanIdol.get_or_none(FanIdol.idol_id==int(idol_id) , FanIdol.fan==self.id)
        

        fanidol.delete_instance()


    @hybrid_property
    def my_idols(self):
        from models.fanidol import FanIdol

        idols = FanIdol.select(FanIdol.idol).where(FanIdol.fan==self.id , FanIdol.approved==True)   
        return User.select().where(User.id.in_(idols)).order_by(User.username.asc())


    @hybrid_property
    def my_fans(self):
        from models.fanidol import FanIdol

        fans=FanIdol.select(FanIdol.fan).where(FanIdol.idol==self.id, FanIdol.approved==True,FanIdol.blocked==False)
        return User.select().where(User.id.in_(fans)).order_by(User.username.asc())

    @hybrid_property
    def pending_idols(self):
        from models.fanidol import FanIdol
        
        pending_idols=FanIdol.select(FanIdol.idol).where(FanIdol.fan==self.id,FanIdol.approved==False)
        
        return User.select().where(User.id.in_(pending_idols))

    @hybrid_property
    def fan_requests(self):
        from models.fanidol import FanIdol

        fan_requests=FanIdol.select(FanIdol.fan).where(FanIdol.idol==self.id,FanIdol.approved==False , FanIdol.blocked==False)
        return User.select().where(User.id.in_(fan_requests))


    def approve(self,fan_id):
        from models.fanidol import FanIdol

        fanidol=FanIdol.get_or_none(FanIdol.idol==self.id,FanIdol.fan==int(fan_id))
        fanidol.approved=True
        fanidol.save()


    @hybrid_property
    def image_feed(self):
        from models.image import Image

        return Image.select().where(Image.user_id.in_(self.my_idols)).order_by(Image.created_at.desc())
        

    @hybrid_property
    def ten_random_users(self):
        
        return User.select().order_by(pw.fn.Random()).limit(6)



    def search_result(self,username):
        name_list=[user.username for user in User.select()]

        s=[]
        for name in name_list:
            if username in name:
                s.append(name)

        return User.select().where(User.username.in_(s))


    @hybrid_property
    def blocked(self):
        from models.fanidol import FanIdol

        fanidol=FanIdol.select(FanIdol.fan).where(FanIdol.idol==self.id,FanIdol.blocked==True)

        return User.select().where(User.id.in_(fanidol))

        







        
        


