from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from pyramid.httpexceptions import (
    HTTPFound, HTTPClientError, HTTPServiceUnavailable)
import requests
from ..sample_data import STOCK_DATA
from ..models import Stock
from . import DB_ERR_MSG
import os


# API_KEY = os.environ.get('API_KEY', '')
API_URL = 'https://api.iextrading.com/1.0'


# Home Screen Controller
@view_config(route_name='home', renderer='../templates/index.jinja2')
def get_homescreen(request):
    return {}


# User Login And Sign up Page.
@view_config(route_name='auth', renderer='../templates/auth.jinja2')
def auth_view(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            print('User: {}, Email: {}, Password(NEVER DO PLAIN\
                    TEXT PASSWORDS!): {}'.format(username, email, password))
            return HTTPFound(location=request.route_url('entries'))
        except KeyError:
            return {}

    if request.method == 'GET':
        try:
            username = request.GET['username']
            password = request.GET['password']
            print('User: {}, Password(NEVER DO PLAIN TEXT PASSWO\
                    RDS!): {}'.format(username, password))
            return HTTPFound(location=request.route_url('entries'))
        except KeyError:
            return {}
    return HTTPFound(location=request.route_url('home'))


@view_config(route_name='stock', renderer='../templates/add-stock.jinja2',
            request_method=('GET', 'POST'))
def stock_view(request):
    if request.method == 'GET':
        try:
            symbol = request.GET['symbol']
        except KeyError:
            return {}
        response = requests.get(API_URL + f'/stock/{ symbol }/company')
        if response.status_code == 200:
            return {
                'company': response.json(),
                }
        return HTTPNotFound()
    if request.method == 'POST':
        if 'symbol' not in request.POST:
            return HTTPClientError()
        symbol = request.POST['symbol']
        response = requests.get(API_URL + f'/stock/{ symbol }/company')
        if response.status_code == 200:
            try:
                query = request.dbsession.query(Stock)
                all_entries = query.filter(Stock.symbol == symbol).one_or_none()
                if all_entries is None:
                    request.dbsession.add(Stock(**response.json()))
                    return {}
                else:
                    return {}
            except DBAPIError:
                return DBAPIError(DB_ERR_MSG, content_type='text/plain', status=500)

        return HTTPNotFound()


@view_config(
    route_name='portfolio', renderer='../templates/portfolio.jinja2',
    request_method='GET'
)
def get_portfolio(request):
    if request.method == 'GET':
        try:
            query = request.dbsession.query(Stock)
            all_entries = query.all()
        except DBAPIError:
            return DBAPIError(DB_ERR_MSG, content_type='text/plain', status=500)

        return {
            'stocks': all_entries
        }


@view_config(
    route_name='stock_detail', request_method='GET',
    renderer='../templates/stock-detail.jinja2'
    )
def more_info(request):
    symbol = request.matchdict['symbol']
    response = requests.get(API_URL + f'/stock/{ symbol }/company')
    if response.status_code == 200:
        return {
            'stocks': response.json(),
        }
    return HTTPServiceUnavailable()
    # for entry in STOCK_DATA:
    #     if entry['symbol'] == symbol:
    #         return {'entry': entry}
    #     return HTTPServiceUnavailable()
