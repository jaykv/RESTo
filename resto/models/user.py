from resto.plugs.mongoframes.frame import SerializedFrame
from resto.model import model, Field
from datetime import datetime


@model()
class Users(SerializedFrame):
    fields = {
        'firstname': (str, ...),
        'lastname': (str, ...),
        'email': str,
        '_created': Field(datetime, alias='created', private=True),
    }
