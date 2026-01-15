import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Establish an application context before running the tests.
        with app.app_context():
            yield client

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'version' in data

def test_get_tasks_empty(client):
    """Test getting tasks list (might be empty or not, depending on order)."""
    response = client.get('/tasks')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_create_task(client):
    """Test creating a new task."""
    payload = {
        "title": "Unit Test Task",
        "description": "Created by Pytest",
        "status": "TODO"
    }
    response = client.post('/tasks', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == "Unit Test Task"
    assert 'id' in data
    return data['id']

def test_task_lifecycle(client):
    """Test full lifecycle: Create -> Get -> Update -> Delete -> Verify."""
    # 1. Create
    payload = {"title": "Lifecycle Task", "status": "TODO"}
    rv = client.post('/tasks', json=payload)
    assert rv.status_code == 201
    task_id = rv.get_json()['id']

    # 2. Get
    rv = client.get(f'/tasks/{task_id}')
    assert rv.status_code == 200
    assert rv.get_json()['title'] == "Lifecycle Task"

    # 3. Update
    update_payload = {"status": "DONE"}
    rv = client.put(f'/tasks/{task_id}', json=update_payload)
    assert rv.status_code == 200
    assert rv.get_json()['status'] == "DONE"

    # 4. Delete
    rv = client.delete(f'/tasks/{task_id}')
    assert rv.status_code == 200

    # 5. Verify Delete
    rv = client.get(f'/tasks/{task_id}')
    assert rv.status_code == 404
