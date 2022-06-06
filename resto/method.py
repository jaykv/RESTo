from dataclasses import dataclass
from typing import TypeVar
from resto.api import spec
from resto.model import Model
from resto.actions import ActionsConnector
from resto.util import BaseUtil

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
            BaseUtil.error(method_params, params)
            results = route.execute(method_params, **params)

            if route.hook:
                return route.hook(results=results, **params)

            return results

        return inner_execute

    @classmethod
    def _get(cls, model, actions, validator, route):
        args = route.args or {}
        filter = route.filter or {}
        query = route.query or {}
        projection = route.projection or {}

        validator_args = {'query': model.farms['Filterable']}
        validator_args.update(validator)

        @spec.rest_validate(**validator_args)
        def inner_get(**params):
            results = actions.fetcher(
                model, args=args, filter=filter, query=query, projection=projection
            )

            if route.hook:
                return route.hook(results=results, **params)

            return results

        return inner_get

    @classmethod
    def _post(cls, model, actions, validator, route):
        def inner_post():
            pass

        return inner_post

    @classmethod
    def _put(cls, model, actions, validator, route):
        def inner_put():
            pass

        return inner_put

    @classmethod
    def _patch(cls, model, actions, validator, route):
        def inner_patch():
            pass

        return inner_patch

    @classmethod
    def _delete(cls, model, actions, validator, route):
        def inner_delete():
            pass

        return inner_delete
