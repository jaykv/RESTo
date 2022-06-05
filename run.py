from resto.plugs.flask import RESToFlask
from resto.plugs.mongoframes import MongoModeler
from resto.controllers import *
from resto.models import *
from resto.api import register_spec

# load models first
MongoModeler.load_models()

app = RESToFlask(__name__, lazy_load=False).app

# if lazy loaded app, load controllers now:
#RESToFlask.load_controllers(app)

spec = register_spec('flask', app)

if __name__ == '__main__':
    app.run(debug=True)

