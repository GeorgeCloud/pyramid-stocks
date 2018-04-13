from pyramid.httpexceptions import HTTPFound, HTTPUnauthorized
from pyramid.security import NO_PERMISSION_REQUIRED, remember, forget
from sqlalchemy.exc import DBAPIError
from pyramid.view import view_config
from ..models import Account


# User Login And Sign up Page.
@view_config(
    route_name='auth',
    renderer='../templates/auth.jinja2',
    permission=NO_PERMISSION_REQUIRED,
    request_method=('GET', 'POST'))
def auth_view(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
        except KeyError:
            return {}
        instance = Account(username=username, email=email, password=password)
        request.dbsession.add(instance)
        try:
            request.dbsession.flush()
        except DBAPIError:
            return {}
        headers = remember(request, userid=instance.username)
    if request.method == 'GET':
        try:
            username = request.GET['user']
            password = request.GET['password']
        except KeyError:
            return {}
        if not Account.check_credentials(request, username, password):
            raise HTTPUnauthorized
        headers = remember(request, userid=username)
    return HTTPFound(location=request.route_url('portfolio'), headers=headers)


@view_config(route_name='logout')
def user_logout(request):
    headers = forget(request)
    return HTTPFound(location=request.route_url('home'), headers=headers)
