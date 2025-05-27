import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from datetime import date

from app.main import app
from app.db.database import get_db
from app.models.inventory import InventoryItem
# Import the actual require_role function to use it as the KEY in dependency_overrides
from app.auth.dependencies import require_role # <--- Make sure this import is correct

client = TestClient(app)

@pytest.fixture
def mock_db_session():
    """Provides a mocked SQLAlchemy session for database operations."""
    mock_session = MagicMock()
    mock_session.query.return_value = MagicMock()
    yield mock_session

@pytest.fixture
def override_inventory_dependencies(mock_db_session):
    """
    Overrides the `get_db` and `require_role` dependencies for inventory tests.
    This fixture ensures that requests are authenticated and authorized as an Administrator.
    """
    # Define the mock for `require_role`.
    # This function will replace the original `require_role` in `app.dependency_overrides`.
    # It must mimic `require_role`'s signature: accepts `roles` and returns a callable.
    def mock_require_role_override(roles: list[str]):
        # This nested function is the actual dependency callable that FastAPI will execute.
        def _mock_user_provider():
            # Return a mock user object with the 'Administrator' role.
            # This directly fulfills the dependency, bypassing real auth/role checks.
            return {"username": "mock_admin", "role": "Administrator", "id": 1}
        return _mock_user_provider # The "factory" returns this inner callable

    # Store original dependencies to restore them later
    original_get_db = app.dependency_overrides.get(get_db)
    original_require_role = app.dependency_overrides.get(require_role)

    # Apply the overrides using app.dependency_overrides
    app.dependency_overrides[get_db] = lambda: mock_db_session
    app.dependency_overrides[require_role] = mock_require_role_override # <--- Direct override here

    yield # This allows the tests to run

    # Clean up the overrides after the tests are finished
    # Restore original dependencies if they existed
    if original_get_db is None:
        app.dependency_overrides.pop(get_db, None)
    else:
        app.dependency_overrides[get_db] = original_get_db

    if original_require_role is None:
        app.dependency_overrides.pop(require_role, None)
    else:
        app.dependency_overrides[require_role] = original_require_role
