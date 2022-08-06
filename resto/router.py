from typing import Callable

from resto.actions import Actions
from resto.controller import Delete, Get, Patch, Post, Route
from resto.method import MethodGenerator
from resto.model import Model


class Router:
    __slots__ = ['routes']

    def __init__(self, *route_list):
        self.routes = set()
        self.add(*route_list)

    def add(self, *route_list):
        valid_routes = filter(lambda route: isinstance(route, Route), route_list)
        list(map(self.routes.add, valid_routes))

    def parse_routes(self, model: type[Model]):
        for route in self.routes:
            self.gen_method(route, model)

    @classmethod
    def gen_method(cls, route: Route, model: type[Model]) -> Callable:

        gen_options = {
            'model': model,
            'actions': route.actions or Actions.connector,
            'validator': route.validator or {},
        }

        generator = MethodGenerator._execute if route.execute else route.GENERATOR
        method = generator(**gen_options, route=route)
        method.__name__ = f'{type(route).__name__}_{route.get_rulename()}_{model.__name__}'

        if route.doc:
            method.__doc__ = route.doc

        return method


class ActionRouter(Router):
    def __init__(
        self,
        model: type[Model],
        tags: list = [],
        Fetcher: bool = True,
        Inserter: bool = True,
        Updater: bool = True,
        Deleter: bool = True,
    ):
        action_routes = []
        if Fetcher:
            action_routes.append(
                Get(
                    rule='/',
                    doc=f"Fetch {model.__name__}",
                    validator={'query': model.farms["Filterable"], 'tags': tags},
                )
            )
        if Inserter:
            action_routes.append(
                Post(
                    rule='/',
                    doc=f"Insert {model.__name__}",
                    validator={'json': model.farms["Insertable"], 'tags': tags},
                )
            )
        if Updater:
            action_routes.append(
                Patch(
                    rule='/<_id>',
                    doc=f"Update {model.__name__} by id",
                    validator={'json': model.farms["Updatable"], 'tags': tags},
                )
            )
        if Deleter:
            action_routes.append(
                Delete(
                    rule='/<_id>', doc=f"Delete {model.__name__} by id", validator={'tags': tags}
                )
            )

        Router.__init__(self, *action_routes)
