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
