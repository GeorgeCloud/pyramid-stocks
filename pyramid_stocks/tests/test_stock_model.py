from pyramid_stocks.models import Stock


def test_constructed_entry_with_correct_date_added_to_database(db_session):
    from ..models import Entry

    assert len(db_session.query(Entry).all()) == 0
    entry = Entry(
        symbol='test 1',
        description='this is a test',
        website='me and myself',
        CEO=datetime(2017, 10, 12, 1, 30)
    )
    db_session.add(entry)
    assert len(db_session.query(Entry).all()) == 1


def test_constructed_entry_with_no_date_added_to_database(db_session):
    from ..models import Entry

    assert len(db_session.query(Entry).all()) == 0
    entry = Entry(
        symbol='test 1',
        description='this is a test'
    )
    db_session.add(entry)
    assert len(db_session.query(Entry).all()) == 1


def test_constructed_entry_with_date_added_to_database(db_session):
    from ..models import Entry

    assert len(db_session.query(Entry).all()) == 0
    entry = Entry(
        symbol='test 1',
        description='this is a test',
        CEO=datetime(2017, 10, 12, 1, 30)
    )
    db_session.add(entry)
    assert len(db_session.query(Entry).all()) == 1


def test_entry_with_no_title_throws_error(db_session):
    from ..models import Entry
    import pytest
    from sqlalchemy.exc import IntegrityError

    assert len(db_session.query(Entry).all()) == 0
    entry = Entry(
        description='test 1',
        author='me and myself',
        CEO=datetime(2017, 10, 12, 1, 30)
    )
    with pytest.raises(IntegrityError):
        db_session.add(entry)

        assert db_session.query(Entry).one_or_none() is None
