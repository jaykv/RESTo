from mongoframes import Frame
from typing import Callable, TypeVar, List, Generic, Union
from resto.actions import DefaultActions, ActionsConnector
from resto.method import MethodGenerator
from resto.util import BaseUtil
from resto.request import RequestProxy
from resto.model import FarmBuilder

__all__ = [
    'Controllers',
    'controller',
    'Route',
    'Router',
    'Get',
    'Post',
    'Put',
    'Patch',
    'Delete',
    'get',
    'post',
    'put',
    'patch',
    'delete',
]

Controllers = set()

Controller = TypeVar('Controller')


class App(Generic[Controller]):
    ASYNC = False

    def __init__(self, name: str, request_proxy, lazy_load: bool = False):
        self.name = name
        self.app = self.build_app()
        self.request_proxy = request_proxy

        if not lazy_load:
            self.load_controllers(Controllers)

        RequestProxy.set_request(request_proxy)

    def get_request_proxy(self):
        return self.request_proxy

    def build_app(self):
        raise NotImplementedError

    def load_controller(self, controller: Controller):
        raise NotImplementedError

    def load_controllers(self, controllers: List[Controller]):
        raise NotImplementedError


def controller(endpoint):
    def register_controller(cls):
        cls.endpoint = endpoint
        Controllers.add(cls)
        return cls

    return register_controller


class Route:
    __slots__ = [
        'rule',
        'actions',
        'validator',
        'methods',
        'execute',
        'options',
        'hook',
    ]

    GENERATOR = MethodGenerator._execute

    def __init__(
        self,
        rule: str,
        methods: list[str],
        actions: ActionsConnector = None,
        validator: dict = None,
        execute: Union[Callable, tuple] = None,
        options: dict = None,
        hook: Callable = None,
    ):
        self.rule = rule
        self.methods = methods
        self.options = options or {}
        self.actions = actions
        self.hook = hook
        self.execute = self.parse_execute(execute)
        self.validator = self.parse_validator(validator)
        

    def is_dynamic(self) -> bool:
        return '<' in self.rule and '>' in self.rule

    def get_rulename(self) -> str:
        return self.rule.replace('/', '_').replace('<', '').replace('>', '')

    def parse_execute(self, execute: Union[Callable, tuple]) -> tuple:
        if not execute:
            return None
        
        if not isinstance(execute, tuple):
            return (execute, None)
        
        return execute
    
    def parse_validator(self, validator: dict) -> dict:
        if not validator:
            return {}
        
        # parse fields schema into pydantic models for query and json validation
        if 'query' in validator and isinstance(validator['query'], dict):
            farm_name = '_'.join(self.methods) + self.get_rulename() + 'Query'
            validator['query'] = FarmBuilder.build_lonely_farm(farm_name, validator['query'])
            
        if 'json' in validator and isinstance(validator['json'], dict):
            farm_name = '_'.join(self.methods) + self.get_rulename() + 'Json'
            validator['json'] = FarmBuilder.build_lonely_farm(farm_name, validator['json']) 
        
        return validator

class Router:
    __slots__ = ['routes']

    def __init__(self, *route_list):
        self.routes = set()
        valid_routes = filter(lambda route: isinstance(route, Route), route_list)
        list(map(self.add, valid_routes))

    def add(self, route: Route):
        self.routes.add(route)

    def parse_routes(self, model: type[Frame]):
        for route in self.routes:
            self.gen_method(route, model)

    @classmethod
    def gen_method(cls, route: Route, model: type[Frame]) -> Callable:
        
        gen_options = {
            'model': model,
            'actions': route.actions or DefaultActions.connector,
            'validator': route.validator or {},
        }

        generator = MethodGenerator._execute if route.execute else route.GENERATOR
        method = generator(**gen_options, route=route)
        method.__name__ = (
            f'{type(route).__name__}_{route.get_rulename()}_{model.__name__}'
        )
        return method


class Get(Route):
    __slots__ = ['args', 'strict_filter', 'query', 'projection']

    GENERATOR = MethodGenerator._get

    def __init__(
        self,
        rule: str,
        args: dict = None,
        query: dict = None,
        strict_filter: dict = None,
        projection: dict = None,
        **route_kwargs,
    ):
        if 'methods' not in route_kwargs:
            route_kwargs['methods'] = ['GET']

        self.rule = rule
        self.args = args
        self.query = query
        self.strict_filter = strict_filter
        self.projection = projection

        Route.__init__(self, rule, **route_kwargs)


class Post(Route):
    GENERATOR = MethodGenerator._post

    def __init__(self, rule, **route_kwargs):
        if 'methods' not in route_kwargs:
            route_kwargs['methods'] = ['POST']

        Route.__init__(self, rule, **route_kwargs)


class Put(Route):
    GENERATOR = MethodGenerator._put

    def __init__(self, rule, **route_kwargs):
        if 'methods' not in route_kwargs:
            route_kwargs['methods'] = ['PUT']

        Route.__init__(self, rule, **route_kwargs)


class Patch(Route):
    GENERATOR = MethodGenerator._patch

    def __init__(self, rule, **route_kwargs):
        if 'methods' not in route_kwargs:
            route_kwargs['methods'] = ['PATCH']

        Route.__init__(self, rule, **route_kwargs)


class Delete(Route):
    GENERATOR = MethodGenerator._delete

    def __init__(self, rule, **route_kwargs):
        if 'methods' not in route_kwargs:
            route_kwargs['methods'] = ['DELETE']

        Route.__init__(self, rule, **route_kwargs)


# from: https://github.com/marciojmo/flask-rest-decorators/blob/main/src/flask_rest_decorators/decorators.py
def get(rule, **options):
    def method_wrapper(f):
        f.__rest_metainfo__ = {
            "rule": rule,
            "name": f.__name__,
            "options": {**options, **{"methods": ["GET"]}},
        }
        return f

    return method_wrapper


def post(rule, **options):
    def method_wrapper(f):
        f.__rest_metainfo__ = {
            "rule": rule,
            "name": f.__name__,
            "options": {**options, **{"methods": ["POST"]}},
        }
        return f

    return method_wrapper


def put(rule, **options):
    def method_wrapper(f):
        f.__rest_metainfo__ = {
            "rule": rule,
            "name": f.__name__,
            "options": {**options, **{"methods": ["PUT"]}},
        }
        return f

    return method_wrapper


def patch(rule, **options):
    def method_wrapper(f):
        f.__rest_metainfo__ = {
            "rule": rule,
            "name": f.__name__,
            "options": {**options, **{"methods": ["PATCH"]}},
        }
        return f

    return method_wrapper


def delete(rule, **options):
    def method_wrapper(f):
        f.__rest_metainfo__ = {
            "rule": rule,
            "name": f.__name__,
            "options": {**options, **{"methods": ["DELETE"]}},
        }
        return f

    return method_wrapper
