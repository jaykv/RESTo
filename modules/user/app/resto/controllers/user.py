from spectree import Response as SpecResponse

from resto.actions import Actions
from resto.api import Response, ResponseModel, spec
from resto.controller import Get, controller, get
from resto.method import MethodParams
from resto.models.user import Users
from resto.router import ActionRouter
from resto.util import BaseUtil


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
    router = ActionRouter(model, ['users'])
    router.add(
        # dynamic get- fetch
        Get('/', doc='fetch users', default_query={'test': 123}),
        # custom executes
        Get('/lambda/<id>', doc='lambda test', execute=lambda id: f'lambda user {id}'),
        # hook exec 1
        Get(
            '/hook/<id>',
            doc='hook execute by id',
            execute=hook_execute,
            hook=test_hook,
            validator={
                'security': {'auth_apiKey': []},
                'query': {'username': (str, ...), 'version': (int, 1)},
                'tags': ['users'],
            },
        ),
        # hook exec 2
        Get(
            '/hookname/<name>',
            doc='hook execute by name',
            execute=hook_execute,
            hook=test_hookname,
            validator={'tags': ['users']},
        ),
    )

    @get(rule='/<id>')
    @spec.validate(resp=SpecResponse(HTTP_200=ResponseModel), tags=['users'])
    def get_user(id):
        '''get user by id'''
        print(id)
        users = Actions.connector.fetcher(Users, default_query={'id': id})
        return Response(users)
