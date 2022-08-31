from spectree import Response as SpecResponse

from resto.actions import Actions
from resto.api import Response, ResponseModel, spec
from resto.controller import Get, controller, get
from resto.method import MethodParams
from resto.models.user import Users
from resto.router import ActionRouter
from resto.util import BaseUtil


def pipes_execute(request, context: MethodParams, **params):
    BaseUtil.error(context, params)
    print(request.headers.get('Authorization'))
    params.update({'success': True})
    BaseUtil.error('results', params)
    return params


def test_pipes(results, **params):
    return results


def test_pipesname(results, **params):
    return params


@controller('/users')
class UserController:
    model = Users
    security = {'auth_apiKey': []}
    router = ActionRouter(model, ['users'])
    router.add(
        # dynamic get- fetch
        Get('/', doc='fetch users', default_query={'test': 123}),
        # custom executes
        Get('/lambda/<id>', doc='lambda test', execute=lambda id: f'lambda user {id}'),
        # pipes exec 1
        Get(
            '/pipes/<id>',
            doc='pipes execute by id',
            execute=pipes_execute,
            pipes=[test_pipes],
            validator={
                'security': {'auth_apiKey': []},
                'query': {'username': (str, ...), 'version': (int, 1)},
                'tags': ['users'],
            },
        ),
        # pipes exec 2
        Get(
            '/pipesname/<name>',
            doc='pipes execute by name',
            execute=pipes_execute,
            pipes=[test_pipesname],
            validator={'tags': ['users']},
        ),
    )

    @get(rule='/<id>')
    @spec.validate(resp=SpecResponse(HTTP_200=ResponseModel), tags=['users'])
    def get_user(id):
        '''get user by id'''
        users = Actions.connector.fetcher(Users, default_query={'id': id})
        return Response(users)
