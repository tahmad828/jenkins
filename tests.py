import pytest
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_home_page(client):
    """Test GET request to home page"""
    response = client.get('/')
    assert response.status_code in (200, 302)  # 200 OK or redirect

def test_add_task(client):
    """Test adding a task/student via form POST"""
    # Simulate a logged-in user if needed
    with client.session_transaction() as sess:
        sess['username'] = 'testuser'

    response = client.post(
        '/',
        data={
            'title': 'Test Task'
        },
        follow_redirects=True
    )

    # Ensure response contains the task title
    assert b'Test Task' in response.data


