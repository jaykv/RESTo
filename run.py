from resto.plugs.flask import RESToFlask, request
from resto.plugs.mongoframes import MongoModeler
from resto.controllers import *
from resto.models import *
from resto.api import register_spec

# load models and actions
MongoModeler.load_models()
MongoModeler.load_actions()

app = RESToFlask(__name__, request_proxy=request, lazy_load=False).app

# if lazy loaded app, load controllers now:
# RESToFlask.load_controllers(app)

spec = register_spec('flask', app)

if __name__ == '__main__':
    app.run(debug=True)
