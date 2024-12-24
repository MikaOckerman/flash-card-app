import pytest
from app import app
from extensions import db
import logging
from models import Flashcard, Category, Tag

@pytest.fixture
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mika:1234@localhost:5432/flashcard_test_db'
    app.config['SECRET_KEY'] = 'fast_flash_frenzy_!88'
    logging.debug("Client Tested")

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            db.session.remove()
            db.drop_all()
            yield client
