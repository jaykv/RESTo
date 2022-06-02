from resto.plugins.flask import build_app, FlaskController
from resto.plugins.mongoframes import MongoModeler
from resto.controllers import *
from resto.models import *

app = build_app(__name__)

MongoModeler.load_models()
FlaskController.load_controllers(app)

if __name__ == '__main__':
    app.run(debug=True)

