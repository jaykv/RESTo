from restfarms.plugins.flask import build_app, FlaskController
from restfarms.plugins.mongoframes import MongoModeler
from restfarms.controllers import *
from restfarms.models import *

app = build_app(__name__)

MongoModeler.load_models()
FlaskController.load_controllers(app)

app.run(debug=True)

