from resto.plugs.flask import build_app, FlaskController
from resto.plugs.mongoframes import MongoModeler
from resto.controllers import *
from resto.models import *
from resto.api import register_spec

app = build_app(__name__)

MongoModeler.load_models()
FlaskController.load_controllers(app)

spec = register_spec('flask', app)

if __name__ == '__main__':
    app.run(debug=True)

