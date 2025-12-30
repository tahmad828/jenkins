import pytest
from app import app, db, Student

@pytest.fixture
def client():
    # Configure app for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # in-memory DB
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # create tables
        yield client
        with app.app_context():
            db.drop_all()  # clean up tables

def test_home_page(client):
    """Test GET request to home page"""
    response = client.get('/')
    # Should redirect to login since session not set
    assert response.status_code == 302 or b'login' in response.data

def test_add_student(client):
    """Test adding a student via POST form data"""
    # First, set session to simulate logged-in user
    with client.session_transaction() as sess:
        sess['username'] = 'testuser'

    # Send form data
    response = client.post(
        '/',
        data={
            'firstname': 'John',
            'lastname': 'Doe',
            'email': 'john@example.com',
            'phone': '1234567890'
        },
        follow_redirects=True
    )

    # Check if student was added
    assert response.status_code == 200
    assert b'John' in response.data
    assert b'Doe' in response.data
    assert b'john@example.com' in response.data
    assert b'1234567890' in response.data

def test_logout_redirect(client):
    """Test logout clears session and redirects"""
    with client.session_transaction() as sess:
        sess['username'] = 'testuser'

    response = client.get('/logout', follow_redirects=True)
    assert b'login' in response.data

