import pytest
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

# Import the actual router, Booking model, get_db, and require_role
from app.api.booking import router
from app.models.booking import Booking # This is the SQLAlchemy model, used for spec=
from app.db.database import get_db # Import the actual get_db dependency
from app.auth.dependencies import require_role # Import the actual require_role dependency

app = FastAPI()
app.include_router(router, prefix="/bookings")

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_user_teacher():
    return {"id": 123, "role": "Teacher", "sub": "teacher1"}

@pytest.fixture
def mock_user_admin():
    return {"id": 1, "role": "Administrator", "sub": "admin1"}

@pytest.fixture
def booking_create_data():
    return {
        "item_id": 1,
        "quantity": 1,
        "booking_date": "2024-06-01T10:00:00",
        "return_date": "2024-06-01T12:00:00",
        "status": "pending"
    }

# This fixture will override require_role for all booking tests that use it
@pytest.fixture
def override_booking_auth(mock_user_teacher, mock_user_admin):
    # This mock_require_role_factory will be placed into app.dependency_overrides
    # It must mimic the signature of require_role: takes `roles` and returns a callable.
    def mock_require_role_factory(roles: list[str]):
        def _inner_mock_dependency():
            # For testing success, we can consistently return an Administrator,
            # as Administrator role typically has all permissions.
            # This ensures both create and list bookings pass authentication.
            return mock_user_admin # Always return the admin user for simplicity in tests

        return _inner_mock_dependency

    # Store original dependency to restore it later
    original_require_role = app.dependency_overrides.get(require_role)

    # Override require_role using its actual function object as the key
    app.dependency_overrides[require_role] = mock_require_role_factory

    yield # This runs the actual test

    # Clean up by restoring original dependency
    if original_require_role is None:
        app.dependency_overrides.pop(require_role, None)
    else:
        app.dependency_overrides[require_role] = original_require_role

