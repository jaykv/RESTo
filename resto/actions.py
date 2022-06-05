from mongoframes import Frame
from resto.api import Response
from resto.util import BaseUtil, RESTError
from bson import ObjectId
from flask import request

class Actions:
    @staticmethod
    def fetcher(model: type[Frame], args: dict, filter: dict, query: dict, projection: dict):
        # get the user args
        request_args = request.context.query
        BaseUtil.error(query)
        return Response(data=[request_args, query])
    
    @staticmethod
    def inserter(model: type[Frame], json_data: dict) -> Frame:
        # validation
        validated_obj = model.Insertable(**json_data)
        if not validated_obj:
            raise RESTError('Invalid object')

        obj = model(**json_data)
        obj.insert()
        return obj

    @staticmethod
    def updater(model: type[Frame], id: str, json_data: dict) -> Frame:
        obj = model.by_id(ObjectId(id))
        for field in json_data:
            if field in model._fields:
                setattr(obj, field, json_data[field])

        obj.update()
        return obj

    @staticmethod
    def deleter(model: type[Frame], id: str, filter: dict) -> Frame:
        obj = model.by_id(ObjectId(id)) if id else model.one(filter)
        obj.delete()
        return obj



    