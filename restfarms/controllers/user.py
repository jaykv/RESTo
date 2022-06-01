from restfarms.models.user import Users
from restfarms.controller import controller, Get, Post, Delete, Router, get
from restfarms.actions import Actions

def exec_test():
    return 'exec'

def post_test():
    return 'post'

def delete_test(id):
    return f'delete {id}'

@controller('/users')
class UserController:
    model = Users
    router = Router(
        Get('/', execute=exec_test),
        Get('/lambda/<id>', execute=lambda id: f'lambda user {id}'),
        Post('/<id>', execute=post_test),
        Delete('/<id>', execute=delete_test)
    )

    @get(rule='/<id>')
    def get_user(id):
        return f'get user {id}'
