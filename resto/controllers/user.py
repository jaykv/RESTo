from resto.models.user import Users
from resto.controller import controller, Get, Post, Delete, Router, get
from resto.api import spec, ResponseModel, Response
from spectree import Response as SpecResponse
from resto.method import MethodParams

from resto.util import BaseUtil


def exec_test():
    return Response(output='exec')


def post_test():
    return 'post'


def delete_test(id):
    return f'delete {id}'


def hook_execute(method_params: MethodParams, **req_args):
    BaseUtil.error(method_params, req_args)
    req_args.update({'success': True})
    BaseUtil.error('results', req_args)
    return req_args


def test_hook(results, **params):
    return Response(results)


def test_hookname(results, **params):
    return Response(params)


@controller('/users')
class UserController:
    model = Users
    router = Router(
        # dynamic get- fetch
        Get('/', query={'test': 123}),
        # custom executes
        Get('/lambda/<id>', execute=lambda id: f'lambda user {id}'),
        # hook exec 1
        Get(
            '/hook/<id>',
            execute=hook_execute,
            hook=test_hook,
            validator={'tags': ['users']},
        ),
        # hook exec 2
        Get(
            '/hookname/<name>',
            execute=hook_execute,
            hook=test_hookname,
            validator={'tags': ['users']},
        ),
        Post('/<id>', execute=post_test),
        Delete('/<id>', execute=delete_test),
    )

    @get(rule='/<id>')
    @spec.validate(resp=SpecResponse(HTTP_200=ResponseModel), tags=['users'])
    def get_user(id):
        return Response(f'get user {id}')
