from operator import index
from unittest.mock import Base
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
from datetime import datetime, timedelta

from utils import credentials as creds

class Users(Base):
    id = fields.IntField(pk=True, index=True)
    username = fields.CharField(50, unique=True)
    hashed_password = fields.CharField(128)

    
class RegisterItem(BaseModel):
    username: str = Field(examples=["username"])
    password: str = Field(default=None, examples=["******"])
    email: str = Field(examples=["your@email.com"])

class LoginItem(BaseModel):
    username: str = Field(examples=["username"])
    password: str = Field(default=None, examples=["******"])

