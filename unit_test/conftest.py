import pytest

from app import create_app, db


@pytest.fixture(scope='function')
def client():
    app = create_app('test')
    client = app.test_client()

    with app.app_context():
        db.drop_all()
        db.create_all()

        yield client  # this is where the testing happens!
