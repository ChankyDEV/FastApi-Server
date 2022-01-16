from tortoise import fields
from tortoise.models import Model
from passlib.hash import bcrypt

class User(Model):
    id = fields.IntField(pk=True)
    uuid = fields.UUIDField()
    username = fields.CharField(50, unique=True)
    password = fields.CharField(128)
    
    def verify_password(self, password):
        return bcrypt.verify(password, self.password)