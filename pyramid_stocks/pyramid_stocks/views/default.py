from pyramid.response import Response
from pyramid.view import view_config
from ..sample_data import STOCK_DATA
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from sqlalchemy.exc import DBAPIError
from ..models import MyModel


@view_config(route_name='home', renderer='../templates/index.jinja2')
def get_homescreen(request):
    return {}


@view_config(route_name='auth', renderer='../templates/auth.jinja2')
def auth_view(request):
    if request.method == 'GET':
        try:
            username = request.GET['username']
            password = request.GET['password']
            print('User: {}, Pass: {}'.format(username, password))

            return HTTPFound(location=request.route_url('portfolio'))

        except KeyError:
            return {}

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        print('User: {}, Pass: {}, Email: {}'.format(username, password, email))

        return HTTPFound(location=request.route_url('portfolio'))

    return HTTPNotFound()


@view_config(route_name='add_stock', renderer='../templates/add-stock.jinja2')
def add_stock(request, stock):
    return {}


@view_config(route_name='stock_detail', renderer='../templates/stock-detail.jinja2')
def more_info(request):
    symbol = request.matchdict['symbol']
    for entry in STOCK_DATA:
        if entry['symbol'] == symbol:
            return {'entry': entry}
    # lst = {}
    # query = request.matchdict['symbol']
    # for el in STOCK_DATA:
    #     if el['symbol'] == query:
    #         lst = el
    # return lst


@view_config(route_name='portfolio', renderer='../templates/portfolio.jinja2')
def get_portfolio(request):
    return {
    'stocks': STOCK_DATA
    }
