from pyramid.httpexceptions import HTTPFound, HTTPBadRequest, HTTPUnauthorized, HTTPClientError, HTTPServiceUnavailable
from pyramid.security import NO_PERMISSION_REQUIRED, remember, forget
from sqlalchemy.exc import DBAPIError
from pyramid.response import Response
from ..sample_data import STOCK_DATA
from pyramid.view import view_config
from ..models import Account
from ..models import Stock
from . import DB_ERR_MSG
import requests
import os


# User Login And Sign up Page.
@view_config(
    route_name='auth',
    renderer='../templates/auth.jinja2',
    permission=NO_PERMISSION_REQUIRED)
def auth_view(request):
    if request.method == 'GET':
        try:
            username = request.GET['username']
            password = request.GET['password']

        except KeyError:
            return {}
        is_authenticated = Account.check_credentials(request, username, password)
        if is_authenticated[0]:
            headers = remember(request, userid=username)
            return HTTPFound(location=request.route_url('portfolio'), headers=headers)
        else:
            return HTTPUnauthorized()

    if request.method == 'POST':
        try:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']

        except KeyError:
            return HTTPBadRequest()
        try:
            instance = Account(
                username=username,
                email=email,
                password=password,
            )
            headers = remember(request, userid=instance.username)
            request.dbsession.add(instance)

            return HTTPFound(location=request.route_url('portfolio'), headers=headers)

        except DBAPIError:
            return Response(DB_ERR_MSG, content_type='text/plain', status=500)


@view_config(route_name='logout')
def user_logout(request):
    headers = forget(request)
    return HTTPFound(location=request.route_url('home'), headers=headers)
