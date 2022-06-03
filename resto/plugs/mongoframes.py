from pymongo import MongoClient
from resto.model import FarmBuilder, Models
from mongoframes import Frame

class MongoModeler:
    @staticmethod
    def load_model(model: type[Frame]):
        # build farms
        farmbuilder = FarmBuilder()
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