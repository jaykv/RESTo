from resto.actions import ActionsConnector
from resto.util import BaseUtil, RESTError
from bson import ObjectId
from mongoframes import Frame


def build_filter_query(filter, projection):
    # TODO
    return filter


class MongoActions(ActionsConnector):
    @staticmethod
    def fetcher(
        model: type[Frame],
        args: dict,
        strict_filter: dict,
        query: dict,
        projection: dict,
    ) -> list[Frame]:
        filter = strict_filter if strict_filter else args
        filter_query = build_filter_query(filter, projection) | query
        docs = model.find_many(filter_query, projection=projection)
        return docs

    @staticmethod
    def inserter(model: type[Frame], data: dict) -> Frame:
        # validation
        validated_obj = model.farms['Insertable'](**data)
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
