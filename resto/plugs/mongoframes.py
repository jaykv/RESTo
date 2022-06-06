from pymongo import MongoClient
from resto.model import FarmBuilder, Models
from resto.actions import ActionsConnector, DefaultActions
from resto.controller import RequestProxy
from resto.util import BaseUtil, RESTError
from resto.api import Response
from bson import ObjectId
from mongoframes import Frame


class MongoActions(ActionsConnector):
    @staticmethod
    def fetcher(
        model: type[Frame], args: dict, filter: dict, query: dict, projection: dict
    ) -> Frame:
        # get the user args
        BaseUtil.error(query)
        return Response(data=[args, query])

    @staticmethod
    def inserter(model: type[Frame], data: dict) -> Frame:
        # validation
        validated_obj = model.Insertable(**data)
        if not validated_obj:
            raise RESTError('Invalid object')

        obj = model(**data)
        obj.insert()
        return obj

    @staticmethod
    def updater(model: type[Frame], id: str, data: dict, upsert: bool = False) -> Frame:
        obj = model.by_id(ObjectId(id))
        for field in data:
            if field in model._fields:
                setattr(obj, field, data[field])

        if upsert:
            obj.upsert()
        else:
            obj.update()

        return obj

    @staticmethod
    def deleter(model: type[Frame], id: str, filter: dict) -> Frame:
        obj = model.by_id(ObjectId(id)) if id else model.one(filter)
        obj.delete()
        return obj


class MongoModeler:
    @staticmethod
    def load_actions():
        DefaultActions.set_connector(MongoActions)

    @staticmethod
    def load_model(model: type[Frame]):
        # load fields
        farmbuilder = FarmBuilder()
        farmbuilder.load_fields(model.fields)

        # build farms
        model.farms = farmbuilder.build_farms(model.__name__)

        # mongoframes model setup
        model._private_fields = farmbuilder.private_fields
        model._fields = farmbuilder.public_fields
        model.farmbuilder = farmbuilder

        return model

    @staticmethod
    def load_models():
        # TODO: switch this to env variable
        Frame._client = MongoClient('mongodb://localhost:27017/testdb')
        return list(map(MongoModeler.load_model, Models))
