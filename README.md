
# RESTo (in development)
Streamlined REST API framework with a focus on reducing boilerplate and fast-tracking CRUD actions with dynamic routes. Synergizes nicely with popular web frameworks and databases (through ORM/ODMs) to support a unified structure to bootstrap REST APIs quickly.

## Current plugins
* Flask (controller loader)
* MongoFrames (model loader)


## Usage

### Model
Models define the schema- fields, properties, and attributes of entities. Define the schema only once- use it for validation, database querying, spec-generation anywhere.

```python
from mongoframes import Frame
from resto.model import model, Field
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
Controllers use a Router and custom method definitions to setup nested API routes under a common endpoint. Additionally links the model for performing DB-based actions dynamically in routes.

```python
from resto.models.user import User
from resto.controller import controller, Get, Post, Delete, Router, get

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
        Get('/', execute=exec_test),
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
from resto.plugins.flask import build_app, FlaskController
from resto.plugins.mongoframes import MongoModeler
from resto.controllers.user import UserController
from resto.models.user import Users

app = build_app(__name__)

# load imported models- parse model to setup fields and generate validation farms
MongoModeler.load_models()

# load imported controllers- build routes from controller dynamically
FlaskController.load_controllers(app)

if __name__ == '__main__':
    app.run(debug=True)
```