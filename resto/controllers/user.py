from resto.models.user import Users
from resto.controller import controller, Get, Post, Delete, Router, get
from resto.api import spec, ResponseModel, Response
from spectree import Response as SpecResponse
from resto.method import MethodParams
from resto.util import BaseUtil

def post_test(request, context: MethodParams, upsert: bool=False, id=None, **params):
    print(request.headers)
    return Response(request=str(request), context=str(context), upsert=upsert, output=f'completed {id}')


def delete_test(id):
    return f'delete {id}'


def hook_execute(request, context: MethodParams, **params):
    BaseUtil.error(context, params)
    print(request.headers.get('Authorization'))
    params.update({'success': True})
    BaseUtil.error('results', params)
    return params


def test_hook(results, **params):
    return Response(results)


def test_hookname(results, **params):
    return Response(params)


@controller('/users')
class UserController:
    model = Users
    security = {'auth_apiKey': []}
    router = Router(
        # dynamic get- fetch
        Get('/', doc='fetch users', query={'test': 123}),
        # custom executes
        Get('/lambda/<id>', doc='lambda test', execute=lambda id: f'lambda user {id}'),
        # hook exec 1
        Get(
            '/hook/<id>',
            doc='hook execute by id',
            execute=hook_execute,
            hook=test_hook,
            validator={'security': {'auth_apiKey': []}, 'query': {'username': (str, ...), 'version': (int, 1)}, 'tags': ['users']},
        ),
        # hook exec 2
        Get(
            '/hookname/<name>',
            doc='hook execute by name',
            execute=hook_execute,
            hook=test_hookname,
            validator={'tags': ['users']},
        ),
        # custom executor
        Post(
            '/<id>', 
            doc='update user by id',
            validator={'json': model.farms['Updatable']}, 
            execute=(post_test, 
                     {'upsert': True})
        ),
        Delete('/<id>', doc='delete user by id', execute=delete_test),
    )

    @get(rule='/<id>')
    @spec.validate(resp=SpecResponse(HTTP_200=ResponseModel), tags=['users'])
    def get_user(id):
        '''get user by id'''
        return Response(f'get user {id}')
