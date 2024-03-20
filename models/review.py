#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import ForeignKey, Column, String
from os import getenv


class Review(BaseModel, Base):
    """ Review classto store review information """
    if getenv("HBNB_TYPE_STORAGE") == "db":
        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        __tablename__ = "reviews"
    else:
        text = ""
        place_id = ""
        user_id = ""
