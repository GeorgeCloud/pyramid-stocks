import pytest
from pyramid import testing
from ..models.meta import Base
from ..models import Stock
from pyramid_stocks.models import Account


@pytest.fixture
def dummy_stock():
    return Stock(
        symbol='CRM',
        companyName='SalesForce',
        description='That Software Company',
        exchange='trade',
        industry='Software Development',
        website='www.google.com/SalesForce.com',
        CEO='Marc Ben',
        issueType='cs',
        sector='lemon',
    )


@pytest.fixture
def configuration(request):
    config = testing.setUp(settings={
        'sqlalchemy.url = postgres://localhost:5432/entries_prod'
    })
    config.include('pyramid_stocks.models')
    config.include('pyramid_stocks.routes')
    yield config
    testing.tearDown()


@pytest.fixture
def db_session(configuration, request):
    """
    Create DB Sesssion.
    """
    SessionFactory = configuration.registry['dbsession_factory']
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)
    yield session
    session.transaction.rollback()
    Base.metadata.drop_all(engine)


@pytest.fixture
def user_session(configuration, request):
    SessionFactory = configuration.registry['dbsession_factory']
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)
    session.add(Account(
        username='john',
        email='johndoe@.com',
        password='helloworld')
    )
    session.commit()
    yield session
    session.transaction.rollback()
    Base.metadata.drop_all(engine)
