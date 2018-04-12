from pyramid.httpexceptions import HTTPFound
from pyramid.view import forbidden_view_config


@forbidden_view_config()
def notfound_view(request):
    return HTTPFound(location=request.route_url('auth'))
