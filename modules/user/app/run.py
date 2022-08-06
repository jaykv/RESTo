from resto.plugs.flask import RESToFlask, request
from resto.plugs.mongoframes import MongoModeler
from resto.controllers import *
from resto.models import *
from resto.api import register_spec, SecurityScheme
import os

# load models and actions
MongoModeler.load_models(mongo_uri=os.environ.get('MONGODB_URI'))
MongoModeler.load_actions()

app = RESToFlask(__name__, request_proxy=request, lazy_load=False).app

# if lazy loaded app, load controllers now:
# RESToFlask.load_controllers(app)

security_schemes = [
    SecurityScheme(
        name="auth_apiKey",
        data={"type": "apiKey", "name": "Authorization", "in": "header"},
    ),
]

spec = register_spec('flask', app, security_schemes=security_schemes)

application = app

if __name__ == '__main__':
    app.run(debug=True)
