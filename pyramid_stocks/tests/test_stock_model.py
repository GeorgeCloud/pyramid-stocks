from pyramid_stocks.models import Stock
from ..models import Stock
import pytest


def test_constructed_entry_with_correct_data_added_to_database(db_session):
    assert len(db_session.query(Stock).all()) == 0
    stock = Stock(
        symbol='CRM',
        description='software company',
        website='crm.com',
        CEO='Marc'
    )
    db_session.add(stock)
    assert len(db_session.query(Stock).all()) == 1


def test_constructed_entry_with_no_website_added_to_database(db_session):
    assert len(db_session.query(Stock).all()) == 0
    stock = Stock(
        symbol='pi',
        description='this is a test'
    )
    db_session.add(stock)
    assert len(db_session.query(Stock).all()) == 1


def test_constructed_entry_with_no_description_to_database(db_session):
    assert len(db_session.query(Stock).all()) == 0
    stock = Stock(
        symbol='X',
        description='Owner of all barns through the bubblegum palace..',
        CEO='barn'
    )
    db_session.add(stock)
    assert len(db_session.query(Stock).all()) == 1


def test_assertion_error(db_session):
    assert len(db_session.query(Stock).all()) == 0
    stock = Stock(
        symbol='msft',
        description='me and myself',
        CEO='johnny'
    )
    with pytest.raises(AssertionError):
        db_session.add(stock)
        assert db_session.query(Stock).one_or_none() is None
