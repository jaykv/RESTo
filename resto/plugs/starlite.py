from typing import List

from starlite import Request
from starlite import Router as StarliteRouter
from starlite import Starlite, handlers

from resto.api import Response
from resto.controller import App, Controller
from resto.router import Router
from resto.util import BaseUtil, RESTError


class RESToStarlite(App):
    def build_app(self, controllers: List[Controller]):
        def handle_resto_error(_: Request, e: RESTError):
            BaseUtil.error(e)
            return Response(error=e, bubble_error=True)

        app = Starlite(
            route_handlers=[controller.__router__ for controller in controllers],
            exception_handlers={RESTError: handle_resto_error},
        )

        return app

    def load_controller(self, controller: Controller):
        # restify controller routes by setting rest metadata
        for route in controller.router.routes:
            method = Router.gen_method(route, controller.model)

            handler = route.methods[0].lower()
            rest_method = getattr(handlers, handler)(method)(route.rule)
            rest_method.__rest__ = True

            setattr(controller, method.__name__, rest_method)

        # build controller blueprint
        methods = [getattr(controller, m) for m in dir(controller) if hasattr(m, '__rest__')]
        controller.__router__ = StarliteRouter(methods)

    def load_controllers(self, controllers: List[Controller]):
        for controller in controllers:
            self.load_controller(controller)
