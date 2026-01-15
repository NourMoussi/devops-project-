import pytest
import uuid
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_request_id_generation(client):
    """Test that a request ID is automatically generated if missing."""
    response = client.get('/health')
    assert response.status_code == 200
    assert 'X-Request-ID' in response.headers
    assert len(response.headers['X-Request-ID']) > 0

def test_request_id_propagation(client):
    """Test that an existing X-Request-ID is propagated."""
    custom_id = str(uuid.uuid4())
    headers = {'X-Request-ID': custom_id}
    
    response = client.get('/health', headers=headers)
    assert response.status_code == 200
    assert response.headers['X-Request-ID'] == custom_id
