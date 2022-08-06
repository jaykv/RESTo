from dataclasses import dataclass
from typing import TypeVar
from resto.api import spec, Response
from resto.model import Model
from resto.actions import ActionsConnector
from resto.util import BaseUtil
from resto.request import RequestProxy

Route = TypeVar('Route')


@dataclass(frozen=True)
class MethodParams:
    model: Model
    actions: ActionsConnector
    route: Route


class MethodGenerator:
    """Dynamic method generators to link each REST method to an action"""

    @classmethod
    def _execute(
        cls,
        model: type[Model],
        actions: type[ActionsConnector],
        validator: dict,
        route: Route,
    ):
        context = MethodParams(model, actions, route)
        execute = route.execute[0]
        execute_params = route.execute[1] or {}
        
        @spec.rest_validate(**validator)
        def inner_execute(**params):
            results = execute(request=RequestProxy.request, context=context, **execute_params, **params)

            if route.hook:
                return route.hook(results=results, **params)

            return Response(data=results)

        return inner_execute

    @classmethod
    def _get(
        cls,
        model: type[Model],
        actions: type[ActionsConnector],
        validator: dict,
        route: Route,
    ):
        default_args = route.default_args or {}
        strict_filter = route.strict_filter or {}
        default_query = route.default_query or {}
        default_projection = route.default_projection or {}

        @spec.rest_validate(**validator)
        def inner_get(**params):
            req_filters = RequestProxy.request.context.query

            results = actions.fetcher(
                model,
                default_args=default_args,
                strict_filter=strict_filter,
                default_query=default_query,
                default_projection=default_projection,
            )
            if route.hook:
                return route.hook(results=results, **params)
            return Response(data=results)

        return inner_get

    @classmethod
    def _post(
        cls,
        model: type[Model],
        actions: type[ActionsConnector],
        validator: dict,
        route: Route,
    ):

        @spec.rest_validate(**validator)
        def inner_post(**params):
            results = actions.inserter(model, data=RequestProxy.request.context.json)
            if route.hook:
                return route.hook(results=results, **params)
            return Response(data=results)

        return inner_post

    @classmethod
    def _patch(
        cls,
        model: type[Model],
        actions: type[ActionsConnector],
        validator: dict,
        route: Route,
    ):
        @spec.rest_validate(**validator)
        def inner_patch(**params):
            results = actions.updater(model, data=RequestProxy.request.context.json)
            if route.hook:
                return route.hook(results=results, **params)
            return Response(data=results)

        return inner_patch

    @classmethod
    def _put(
        cls,
        model: type[Model],
        actions: type[ActionsConnector],
        validator: dict,
        route: Route,
    ):
        @spec.rest_validate(**validator)
        def inner_put(**params):
            results = actions.updater(
                model, data=RequestProxy.request.context.json, upsert=True
            )
            if route.hook:
                return route.hook(results=results, **params)
            return Response(data=results)

        return inner_put

    @classmethod
    def _delete(
        cls,
        model: type[Model],
        actions: type[ActionsConnector],
        validator: dict,
        route: Route,
    ):
        @spec.rest_validate(**validator)
        def inner_delete(**params):
            results = actions.deleter(model, filter=RequestProxy.request.context.json)
            if route.hook:
                return route.hook(results=results, **params)
            return Response(data=results)

        return inner_delete
