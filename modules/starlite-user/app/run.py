import os

import uvicorn

from resto.controller import Controllers
from resto.plugs.mongoframes import MongoModeler
from resto.plugs.starlite import Request, RESToStarlite

# load models and actions
MongoModeler.load_models(mongo_uri=os.environ.get('MONGODB_URI'))
MongoModeler.load_actions()

resto = RESToStarlite(__name__, request_proxy=Request, lazy_load=True)
resto.load_controllers(Controllers)
app = resto.build_app(Controllers)

# security_schemes = [
#     SecurityScheme(
#         name="auth_apiKey",
#         data={"type": "apiKey", "name": "Authorization", "in": "header"},
#     ),
# ]

# spec = register_spec('flask', app, security_schemes=security_schemes)

if __name__ == "__main__":
    uvicorn.run("run:app", port=5000, log_level="info")
