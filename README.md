
# RESTFarms (in development)
Streamlined REST API framework with a focus on reducing boilerplate and providing flexibility with plug-and-play plugins. Primary focus is to synergize with popular web frameworks and databases (through ORM/ODMs) to support a unified structure to bootstrap REST APIs quickly.

## Current plugins
* Flask (controller loader)
* MongoFrames (model loader)


## Usage

### Model
Models define the schema- fields, properties, and attributes of entities. Define the schema only once- use it for validation, database querying, spec-generation anywhere.

```python
from mongoframes import Frame
from restfarms.model import model, Field
from datetime import datetime

@model
class User(Frame):
    fields = {
        'firstname': (str, ...), # required field
        'lastname': (str, ...),
        'email': str, # optional field
        '_created': Field(datetime, alias='created', private=True) # private field
    }
```

### Controller
Controllers define a structure of routes to form an API based on a model and router. Additionally links the model for performing DB-based actions dynamically.

```python
from restfarms.models.user import User
from restfarms.controller import controller, Get, Post, Delete, Router, get

def exec_test():
    return 'exec'

def post_test():
    return 'post'

def delete_test(id):
    return f'delete {id}'

@controller('/users')
class UserController:
    model = User
    router = Router(
        Get(/', execute=exec_test),
        Get('/lambda/<id>', execute=lambda id: id),
        Post('/<id>', execute=post_test),
        Delete('/<id>', execute=delete_test)
    )

    @get(rule='/<id>')
    def get_user(id):
        return f'get user {id}'
```

### App Runner

```python
from restfarms.plugins.flask import build_app, FlaskController
from restfarms.plugins.mongoframes import MongoModeler
from restfarms.controllers.user import UserController
from restfarms.models.user import Users

app = build_app(__name__)

# load imported models- parse model to setup fields and generate validation farms
MongoModeler.load_models()

# load imported controllers- build routes from controller dynamically
FlaskController.load_controllers(app)

if __name__ == '__main__':
    app.run(debug=True)
```