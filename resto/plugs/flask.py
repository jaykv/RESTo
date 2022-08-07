from typing import List

from flask import Blueprint, Flask

from resto.api import Response
from resto.controller import App, Controller
from resto.router import Router
from resto.util import BaseUtil, RESTError


class RESToFlask(App):
    def build_app(self):
        app = Flask(self.name)

        @app.errorhandler(RESTError)
        def handle_error(e: RESTError):
            BaseUtil.error(e)
            return Response(error=e, bubble_error=True)

        return app

    def load_controller(self, controller: Controller):
        # based on https://github.com/marciojmo/flask-rest-decorators
        controller.__blueprint__ = Blueprint(
            controller.__name__, controller.__module__, url_prefix=controller.endpoint
        )
        controller.register_routes = lambda app: app.register_blueprint(controller.__blueprint__)

        # restify controller routes by setting rest metadata
        for route in controller.router.routes:
            method = Router.gen_method(route, controller.model)

            method.__rest_metainfo__ = {
                'rule': route.rule,
                'name': method.__name__,
                'options': {**route.options, **{'methods': route.methods}},
            }

            setattr(controller, method.__name__, method)

        # build controller blueprint
        methods = [getattr(controller, m) for m in dir(controller)]
        for m in methods:
            if hasattr(m, '__rest_metainfo__'):
                controller.__blueprint__.add_url_rule(
                    m.__rest_metainfo__['rule'],
                    m.__rest_metainfo__['name'],
                    m,
                    **m.__rest_metainfo__['options'],
                )

    def load_controllers(self, controllers: List[Controller]):
        for controller in controllers:
            self.load_controller(controller)
            controller.register_routes(self.app)
