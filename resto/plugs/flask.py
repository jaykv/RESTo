from flask import Flask, Blueprint
from resto.controller import Controllers, Router
from resto.util import BaseUtil, RESTError

def build_app(name):
    app = Flask(name)

    @app.errorhandler(RESTError)
    def handle_error(e):
        BaseUtil.error(e)
        return f'ERROR: {e}'

    return app

class FlaskController:
    @staticmethod
    def load_controller(controller):
        # based on https://github.com/marciojmo/flask-rest-decorators
        controller.__blueprint__ = Blueprint( controller.__name__, controller.__module__, url_prefix = controller.endpoint )
        controller.register_routes = lambda app: app.register_blueprint(controller.__blueprint__)

        # restify controller routes by setting rest metadata
        for route in controller.router.routes:
            method = Router.gen_method(route, controller.model)
            
            method.__rest_metainfo__ = {
                'rule': route.rule,
                'name': method.__name__,
                'options': {
                    **route.options,
                    **{ 'methods': route.methods }
                }
            }

            setattr(controller, method.__name__, method)
            
        # build controller blueprint
        methods = [getattr(controller, m) for m in dir(controller)]
        for m in methods:
            if (hasattr(m, '__rest_metainfo__')):
                controller.__blueprint__.add_url_rule( m.__rest_metainfo__['rule'], m.__rest_metainfo__['name'], m, **m.__rest_metainfo__['options'])

    @staticmethod
    def load_controllers(app):
        for controller in Controllers:
            FlaskController.load_controller(controller)
            controller.register_routes(app)