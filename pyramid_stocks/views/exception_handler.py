from pyramid.httpexceptions import HTTPClientError
from pyramid.response import Response
from pyramid.view import exception_view_config
from sqlalchemy.exc import DBAPIError

from . import DB_ERR_MSG


@exception_view_config(
    DBAPIError,
    renderer='../templates/exception-view.jinja2')
def dbapierror_view(request):
    return Response(DB_ERR_MSG, content_type='text/plain', status=500)


@exception_view_config(
    HTTPClientError,
    renderer='../templates/exception-view.jinja2')
def clienterror_view(request):
    return {'error': str(request.exception)}
