# tests/test_main.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the School Inventory Management API"}

def test_cors_headers():
    test_origin = "http://example.com" # Define the origin you're sending

    response = client.options(
        "/",
        headers={
            "Origin": test_origin, # Use the defined origin
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "X-Requested-With"
        }
    )
    assert response.status_code == 200

    headers = {k.lower(): v for k, v in response.headers.items()}

    assert "access-control-allow-origin" in headers
    # CORRECT ASSERTION: When allow_credentials is True and allow_origins includes "*",
    # the middleware echoes the Origin header from the request.
    assert headers["access-control-allow-origin"] == test_origin

    assert "access-control-allow-methods" in headers
    assert "GET" in headers["access-control-allow-methods"]