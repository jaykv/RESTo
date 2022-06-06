from mongoframes import Frame
from typing import Callable, TypeVar, List, Generic
from resto.api import spec
from resto.actions import DefaultActions, ActionsConnector

__all__ = ['Controllers', 'controller', 'Route', 'Router', 'Get', 'Post', 'Put', 'Patch', 'Delete', 
    'get', 'post', 'put', 'patch', 'delete']

Controllers = set()

class RequestProxyLoader:
    def __init__(self):
        self.request = None
    
    def set_request(self, request_proxy):
        self.request = request_proxy
        return self.request
    
RequestProxy: RequestProxyLoader = RequestProxyLoader()

Controller = TypeVar('Controller')
class App(Generic[Controller]):
    ASYNC = False
    
    def __init__(self, name: str, request_proxy, lazy_load: bool=False):
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
 
class MethodGenerator:
    """Dynamic method generators to link each REST method to an action"""
    def _execute():
        def inner_execute():
            pass
        return inner_execute   
    
    def _get(model, actions, args=None, filter=None, query=None, projection=None):
        @spec.rest_validate(query=model.farms['Filterable'])
        def inner_get():
            return actions.fetcher(model, args=args, filter=filter, query=query, projection=projection)
        
        return inner_get
    
    def _post():
        def inner_post():
            pass
        return inner_post
    
    def _put():
        def inner_put():
            pass
        return inner_put
    
    def _patch():
        def inner_patch():
            pass
        return inner_patch
    
    def _delete():
        def inner_delete():
            pass
        return inner_delete
    
class Route():
    __slots__ = ['rule', 'actions', 'methods', 'execute', 'options']

    def __init__(self, rule: str, methods: list[str], actions: ActionsConnector=None, execute: Callable=None, options: dict=None):
        self.rule = rule
        self.methods = methods
        self.execute = execute
        self.options = options or {}
        self.actions = actions
        
    def get_name(self):
        return self.rule.replace('/', '').replace('<', '').replace('>', '')

class Router():
    __slots__ = ['routes']

    def __init__(self, *route_list):
        self.routes = set()
        valid_routes = filter(lambda route: isinstance(route, Route), route_list)
        list(map(self.add, valid_routes))

    def add(self, route: Route):
        self.routes.add(route)
        
    @classmethod
    def gen_method(cls, route: Route, model: type[Frame]):
        gen_options = {
            'model': model,
            'actions': route.actions or DefaultActions.connector,
        }
                    
        if route.execute:
            return route.execute
        
        if isinstance(route, Get):
            gen_options.update({
                'args': route.args or {},
                'filter': route.filter or {},
                'query': route.query or {},
                'projection': route.projection or {}
            })
            
            method =  MethodGenerator._get(**gen_options)
            method.__name__ = f'GET_{route.get_name()}_{model.__name__}'
            return method
        
    def parse_routes(self, model: type[Frame]):
        for route in self.routes:
            self.gen_method(route, model)
        
class Get(Route):
    __slots__ = ['args', 'filter', 'query', 'projection']
    
    def __init__(self, rule, **rargs):
        if 'methods' not in rargs:
            rargs['methods'] = ['GET']
            
        for slot in Get.__slots__:
            if slot in rargs:
                setattr(self, slot, rargs.pop(slot))
            else:
                # TODO: don't waste space storing None?
                setattr(self, slot, None)
            
        Route.__init__(self, rule, **rargs)

class Post(Route):
    def __init__(self, rule, **rargs):
        if 'methods' not in rargs:
            rargs['methods'] = ['POST']
            
        Route.__init__(self, rule, **rargs)

class Put(Route):
    def __init__(self, rule, **rargs):
        if 'methods' not in rargs:
            rargs['methods'] = ['PUT']
            
        Route.__init__(self, rule, **rargs)

class Patch(Route):
    def __init__(self, rule, **rargs):
        if 'methods' not in rargs:
            rargs['methods'] = ['PATCH']
            
        Route.__init__(self, rule, **rargs)

class Delete(Route):
    def __init__(self, rule, **rargs):
        if 'methods' not in rargs:
            rargs['methods'] = ['DELETE']
            
        Route.__init__(self, rule, **rargs)

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