from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from pyramid.security import NO_PERMISSION_REQUIRED, remember, forget
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


@view_config(
    route_name='add-stock',
    renderer='../templates/add-stock.jinja2',
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
