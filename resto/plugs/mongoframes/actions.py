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
        default_args: dict = None,
        strict_filter: dict = None,
        default_query: dict = None,
        default_projection: dict = None,
    ) -> list[Frame]:
        filter = strict_filter if strict_filter else default_args
        filter_query = build_filter_query(filter, default_projection) | default_query
        docs = model.find(filter_query, projection=default_projection)
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
    def updater(
        model: type[Frame],
        obj: Frame = None,
        id: str = None,
        data: dict = None,
        upsert: bool = False,
    ) -> Frame:
        _obj = obj or model.by_id(ObjectId(id))
        for field in data:
            if field in model._fields:
                setattr(_obj, field, data[field])

        if upsert:
            _obj.upsert()
        else:
            _obj.update()

        return _obj

    @staticmethod
    def deleter(
        model: type[Frame], filter: dict = None, obj: Frame = None, id: str = None
    ) -> Frame:
        _obj = obj or model.by_id(ObjectId(id)) if id else model.one(filter)
        _obj.delete()
        return _obj
