
# RESTo (in development)
RESTo makes it easy to build REST APIs quickly without worrying about the boring stuff. It provides structured abstractions to build flexible and dynamic routes based on your defined models and relations. Synergizes nicely with popular web frameworks and ORM/ODMs to support a plug-and-play approach to developing APIs.

## Features
* Structured route builder
* Dynamic CRUD routes generation and configuration
* Built-in request & response validation
* SQL/NoSQL ORM/ODM support to perform DB operations
* Customizable plugs

### Todo:
* Base CRUD routes generation based on controller configuration
* Model relationships
* Dynamic cascades based on Model rules
* Search flags to support flexible data-filtering through endpoint args
* SQLalchemy support (model connector)
* Falcon and Starlette support (controller connectors)
 
## Plugs
Plugs are external frameworks and database ORM/ODMs that "plug" into the RESTo framework through connectors. Connectors bridge the gap between RESTo's abstraction layer- linking the frameworks through an interface for either AppBuilder/Controller or Actions/Model.

### Current Plugs
* Flask (controller connector)
* MongoFrames (model connector)

## Usage

### Model
Models define the schema- fields, properties, and attributes of entities. Define the schema only once- use it for validation, database querying, spec-generation anywhere.

```python
from mongoframes import Frame
from resto.model import model, Field
from datetime import datetime

@model()
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
from resto.models.user import Users
from resto.controller import controller, Get, Post, Delete, Router, get
from resto.api import spec, ResponseModel, Response
from spectree import Response as SpecResponse

@spec.validate(resp=SpecResponse(HTTP_200=ResponseModel), tags=['users'])
def exec_test():
    return Response(output='exec')

def post_test():
    return 'post'

def delete_test(id):
    return f'delete {id}'

@controller('/users')
class UserController:
    model = Users
    router = Router(
        # dynamic get- fetch
        Get('/', query={'test': 123}), 
        
        # custom executes
        Get('/lambda/<id>', execute=lambda id: f'lambda user {id}'),
        Post('/<id>', execute=post_test),
        Delete('/<id>', execute=delete_test)
    )

    @get(rule='/<id>')
    @spec.validate(resp=SpecResponse(HTTP_200=ResponseModel), tags=['users'])
    def get_user(id):
        return Response(f'get user {id}')
```

### App Runner

```python
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
```