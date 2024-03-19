#!/usr/bin/python3
"""
Contains class BaseModel
"""

from datetime import datetime
import models
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid

if models.storage_t == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """BaseModel class"""
    if models.storage_t == "db":
        id = Column(String(60),
                    nullable=False,
                    primary_key=True)
        created_at = Column(DateTime,
                            default=datetime.now,
                            nullable=False)
        updated_at = Column(DateTime,
                            default=datetime.now,
                            nullable=False)

    def __init__(self, *args, **kwargs):
        """init BaseModel"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"],
                                                    "%Y-%m-%dT%H:%M:%S.%f")
            else:
                self.created_at = datetime.now()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"],
                                                    "%Y-%m-%dT%H:%M:%S.%f")
            else:
                self.updated_at = datetime.now()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())

    def __str__(self):
        """print BaseModel"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """save BaseModel"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, save_fs=None):
        """dict BaseModel"""
        my_dict = self.__dict__.copy()
        if "created_at" in my_dict:
            my_dict["created_at"] = my_dict["created_at"].strftime(
                                                    "%Y-%m-%dT%H:%M:%S.%f")
        if "updated_at" in my_dict:
            my_dict["updated_at"] = my_dict["updated_at"].strftime(
                                                    "%Y-%m-%dT%H:%M:%S.%f")
        my_dict["__class__"] = self.__class__.__name__
        if save_fs is None:
            if "password" in my_dict:
                del my_dict["password"]

        return my_dict

    def delete(self):
        """delete BaseModel"""
        models.storage.delete(self)
