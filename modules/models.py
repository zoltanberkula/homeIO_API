from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from enum import unique
from tortoise import fields
from passlib.hash import bcrypt
from tortoise.contrib.pydantic.creator import pydantic_model_creator
from tortoise.models import Model
import jwt
from pydantic import BaseModel, Field
from typing import List
import os

from utils import credentials as creds

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    password_hash = fields.CharField(128)

    @classmethod
    async def get_user(cls, username: str):
        return cls.get(username=username)
    
    def verify_password(self, password: str):
        return bcrypt.verify(password, self.password_hash)
    
User_Pydantic = pydantic_model_creator(User, name='User')
UserIn_Pydantic = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

