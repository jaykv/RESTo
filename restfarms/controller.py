from typing import Callable

__all__ = ['Controllers', 'controller', 'Route', 'Router', 'Get', 'Post', 'Put', 'Patch', 'Delete', 
    'get', 'post', 'put', 'patch', 'delete']

Controllers = set()

def controller(endpoint):
    def register_controller(cls):
        cls.endpoint = endpoint
        Controllers.add(cls)
        return cls
    return register_controller

class Route():
    __slots__ = ['rule', 'methods', 'execute', 'options']

    def __init__(self, rule: str, methods: list[str], execute: Callable, options: dict=None):
        self.rule = rule
        self.methods = methods
        self.execute = execute
        self.options = options or {}

class Router():
    __slots__ = ['routes']

    def __init__(self, *route_list):
        self.routes = set()
        valid_routes = filter(lambda route: isinstance(route, Route), route_list)
        list(map(self.add, valid_routes))

    def add(self, route: Route):
        self.routes.add(route)

class Get(Route):
    def __init__(self, **rargs):
        if 'methods' not in rargs:
            rargs['methods'] = ['GET']
            
        Route.__init__(self, **rargs)

class Post(Route):
    def __init__(self, **rargs):
        if 'methods' not in rargs:
            rargs['methods'] = ['POST']
            
        Route.__init__(self, **rargs)

class Put(Route):
    def __init__(self, **rargs):
        if 'methods' not in rargs:
            rargs['methods'] = ['PUT']
            
        Route.__init__(self, **rargs)

class Patch(Route):
    def __init__(self, **rargs):
        if 'methods' not in rargs:
            rargs['methods'] = ['PATCH']
            
        Route.__init__(self, **rargs)

class Delete(Route):
    def __init__(self, **rargs):
        if 'methods' not in rargs:
            rargs['methods'] = ['DELETE']
            
        Route.__init__(self, **rargs)

# from: https://github.com/marciojmo/flask-rest-decorators/blob/main/src/flask_rest_decorators/decorators.py
def get(rule, **options):
    def method_wrapper(f):
        f.__rest_metainfo__ = {
            "rule": rule,
            "name": f.__name__,
            "options": {
                **options,
                **{ "methods": [ "GET" ] }
            }
        }
        return f
    return method_wrapper

def post(rule, **options):
    def method_wrapper(f):
        f.__rest_metainfo__ = {
            "rule": rule,
            "name": f.__name__,
            "options": {
                **options,
                **{ "methods": [ "POST" ] }
            }
        }
        return f
    return method_wrapper

def put(rule, **options):
    def method_wrapper(f):
        f.__rest_metainfo__ = {
            "rule": rule,
            "name": f.__name__,
            "options": {
                **options,
                **{ "methods": [ "PUT" ] }
            }
        }
        return f
    return method_wrapper

def patch(rule, **options):
    def method_wrapper(f):
        f.__rest_metainfo__ = {
            "rule": rule,
            "name": f.__name__,
            "options": {
                **options,
                **{ "methods": [ "PATCH" ] }
            }
        }
        return f
    return method_wrapper

def delete(rule, **options):
    def method_wrapper(f):
        f.__rest_metainfo__ = {
            "rule": rule,
            "name": f.__name__,
            "options": {
                **options,
                **{ "methods": [ "DELETE" ] }
            }
        }
        return f
    return method_wrapper