from typing import Any, List
from spectree import SpecTree, Response as SpecResponse
from spectree.plugins import PLUGINS as SPEC_PLUGINS
from spectree.config import Configuration
from pydantic import BaseModel
from resto.util import BaseUtil


class RESTSpecTree(SpecTree):
    def rest_validate(self, **kwargs):
        if 'resp' in kwargs:
            return self.validate(**kwargs)
        else:
            return self.validate(resp=SpecResponse(HTTP_200=ResponseModel), **kwargs)


spec = RESTSpecTree()


class ResponseModel(BaseModel):
    data: List[Any]
    messages: List[str]


def Response(
    data: Any = None,
    messages: Any = None,
    error: bool = False,
    status_code: int = 200,
    **raw_data
) -> ResponseModel:
    response_data = [raw_data]
    if data:
        response_data += BaseUtil.listify(data)

    response_messages = ['SUCCESS'] if not error else ['ERROR']
    if messages:
        response_messages += BaseUtil.listify(messages)

    return ResponseModel(data=response_data, messages=response_messages), status_code


def register_spec(plug, app, **kwargs) -> SpecTree:
    spec.backend_name = plug
    spec.backend = SPEC_PLUGINS[plug](spec)
    spec.config = Configuration.parse_obj(kwargs)
    spec.register(app)
    return spec
