from mongoframes import Frame
from resto.model import model, Field
from datetime import datetime

@model
class Users(Frame):
    fields = {
        'firstname': (str, ...),
        'lastname': (str, ...),
        'email': str,
        '_created': Field(datetime, alias='created', private=True)
    }