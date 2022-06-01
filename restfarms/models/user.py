from mongoframes import Frame
from restfarms.model import model, Field
from datetime import datetime

@model
class User(Frame):
    fields = {
        'firstname': (str, ...),
        'lastname': (str, ...),
        'email': str,
        '_created': Field(datetime, alias='created')
    }