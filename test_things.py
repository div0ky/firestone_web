import os
from datetime import datetime, timedelta
from app.models import License
from app import db

import pytest

from app import create_app
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app_test.db'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class SharedVariables(object):
    def __init__(self):
        self.key = '64844D65-076B4102-BDA8EDA3-985FB1B2'
        self.email = 'wildfireajs@gmail.com'
        self.country = 'United States'
        self.order_number = '1234567890'
        self.last_seen = datetime.utcnow()
shared = SharedVariables()

@pytest.fixture
def app():
    app = create_app()
    app.config.from_object(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client():
    app = create_app()
    app.config.from_object(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        # db.session.remove()
        # db.drop_all()

def test_testing_config(app):
    assert app.config['TESTING']

def test_add_license(app):
    new_license = License(license_key=shared.key, email=shared.email, order_number=shared.order_number, country=shared.country, last_seen=shared.last_seen)
    db.session.add(new_license)
    db.session.commit()
    _license = License.query.filter_by(license_key=shared.key).first()
    assert _license is not None

def test_keep_alive(client):
    resp = client.get(f'/alive?key={shared.key}')
    assert b'has been updated' in resp.data
    _license = License.query.filter_by(license_key=shared.key).first()
    assert _license.last_seen + timedelta(minutes=1) >= datetime.utcnow()

def test_map_nodes(client):
    resp = client.get(f'/map?key={shared.key}')
    assert b'nodes' in resp.data

def test_invalid_license(client):
    resp = client.get(f'/alive?key=12341235132451235125')
    assert b'Provided license key is invalid' in resp.data
