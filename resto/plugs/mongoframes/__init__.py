from pymongo import MongoClient
from resto.model import FarmBuilder, Models
from resto.actions import DefaultActions
from mongoframes import Frame
from .actions import MongoActions


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