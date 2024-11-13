#!/usr/bin/python3
"""
defines the class user
"""


from models.base_model import BaseModel


class User(BaseModel):
    """defines class user attributes"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
