from dataclasses import dataclass
from typing import TypeVar
from resto.api import spec
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
        method_params = MethodParams(model, actions, route)

        @spec.rest_validate(**validator)
        def inner_execute(**params):
            results = route.execute(method_params, **params)

            if route.hook:
                return route.hook(results=results, **params)

            return results

        return inner_execute

    @classmethod
    def _get(
        cls,
        model: type[Model],
        actions: type[ActionsConnector],
        validator: dict,
        route: Route,
    ):
        args = route.args or {}
        strict_filter = route.strict_filter or {}
        query = route.query or {}
        projection = route.projection or {}

        validator_args = {'query': model.farms['Filterable']}
        validator_args.update(validator)

        @spec.rest_validate(**validator_args)
        def inner_get(**params):
            req_filters = RequestProxy.request.context.query

            results = actions.fetcher(
                model,
                args=args,
                strict_filter=strict_filter,
                query=query,
                projection=projection,
            )
            if route.hook:
                return route.hook(results=results, **params)
            return results

        return inner_get

    @classmethod
    def _post(
        cls,
        model: type[Model],
        actions: type[ActionsConnector],
        validator: dict,
        route: Route,
    ):

        validator_args = {'json': model.farms['Insertable']}
        validator_args.update(validator)

        @spec.rest_validate(**validator_args)
        def inner_post(**params):
            results = actions.inserter(model, data=RequestProxy.request.context.json)
            if route.hook:
                return route.hook(results=results, **params)
            return results

        return inner_post

    @classmethod
    def _patch(
        cls,
        model: type[Model],
        actions: type[ActionsConnector],
        validator: dict,
        route: Route,
    ):

        validator_args = {'json': model.farms['Updatable']}
        validator_args.update(validator)

        def inner_patch(**params):
            results = actions.updater(model, data=RequestProxy.request.context.json)
            if route.hook:
                return route.hook(results=results, **params)
            return results

        return inner_patch

    @classmethod
    def _put(
        cls,
        model: type[Model],
        actions: type[ActionsConnector],
        validator: dict,
        route: Route,
    ):

        validator_args = {'json': model.farms['Updatable']}
        validator_args.update(validator)

        def inner_put(**params):
            results = actions.updater(
                model, data=RequestProxy.request.context.json, upsert=True
            )
            if route.hook:
                return route.hook(results=results, **params)
            return results

        return inner_put

    @classmethod
    def _delete(
        cls,
        model: type[Model],
        actions: type[ActionsConnector],
        validator: dict,
        route: Route,
    ):
        def inner_delete(**params):
            results = actions.deleter(model, filter=RequestProxy.request.context.json)
            if route.hook:
                return route.hook(results=results, **params)
            return results

        return inner_delete
