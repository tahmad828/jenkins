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
    assert response.status_code == 200
    assert response.is_json

def test_add_task(client):
    """Test adding a task via JSON POST"""
    response = client.post(
        '/',
        json={'title': 'Test Task'}
    )

    # Should return 201 CREATED
    assert response.status_code == 201
    assert response.is_json
    assert response.get_json()['message'] == 'Task added'

    # Verify task exists in database
    get_response = client.get('/')
    tasks = get_response.get_json()
    assert any(t['title'] == 'Test Task' for t in tasks)
