from pymongo import MongoClient
from resto.model import FarmBuilder, Models
from resto.actions import Actions
from mongoframes import Frame
from .actions import MongoActions


class MongoModeler:
    @staticmethod
    def load_actions():
        Actions.set_connector(MongoActions)

    @staticmethod
    def load_model(model: type[Frame]):
        # mongoframes model setup
        model._private_fields = model.farmbuilder.private_fields
        model._fields = model.farmbuilder.public_fields
        return model

    @staticmethod
    def load_models(mongo_uri: str):
        Frame._client = MongoClient(mongo_uri)
        return list(map(MongoModeler.load_model, Models))
