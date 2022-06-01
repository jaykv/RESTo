from restfarms.models.user import User
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
    model = User
    router = Router(
        Get(rule='/', execute=exec_test),
        Get(rule='/lambda/<id>', execute=lambda id: id),
        Post(rule='/<id>', execute=post_test),
        Delete(rule='/<id>', execute=delete_test)
    )

    @get(rule='/<id>')
    def get_user(id):
        return f'get user {id}'
