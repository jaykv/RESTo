from datetime import datetime

from resto.model import Field, model
from resto.plugs.mongoframes.frame import SerializedFrame


@model()
class Users(SerializedFrame):
    fields = {
        'firstname': (str, ...),
        'lastname': (str, ...),
        'email': str,
        '_created': Field(datetime, alias='created', private=True),
    }
