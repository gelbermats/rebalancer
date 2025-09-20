import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.mark.integration
class TestMainApplication:
    
    def test_app_startup(self):
        with TestClient(app) as client:
            response = client.get('/docs')
            assert response.status_code == 200
    
    def test_health_check(self):
        with TestClient(app) as client:
            response = client.get('/')
            assert response.status_code in [200, 404]
    
    @pytest.mark.api
    def test_api_routes_registered(self):
        with TestClient(app) as client:
            response = client.get('/openapi.json')
            assert response.status_code == 200
            
            schema = response.json()
            assert 'paths' in schema
            
            paths = schema['paths']
            expected_prefixes = [
                '/marketdata',
                '/portfolio', 
                '/strategy',
                '/orders',
                '/reporting'
            ]
