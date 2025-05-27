import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app.api.user import router
from app.models.user import User
from fastapi import FastAPI
# No need to import require_role directly from app.auth.dependencies here if patching where used

# Create a FastAPI app instance and include the user router
app = FastAPI()
app.include_router(router, prefix="/users")

@pytest.fixture
def client():
    """Provides a TestClient instance for the FastAPI app."""
    return TestClient(app)

@pytest.fixture
def mock_users():
    """Provides a list of mock User objects for testing."""
    return [
        User(id=1, username="admin", full_name="Admin User", role="Administrator", password="hashed_password_1"),
        User(id=2, username="user1", full_name="Regular User", role="User", password="hashed_password_2"),
    ]

# This fixture will override the `require_role` dependency for the user tests.
@pytest.fixture
def override_user_dependencies():
    """
    Overrides the `require_role` dependency for user route tests.
    This ensures requests are authorized as an Administrator.
    """
    # This function will replace `app.api.user.require_role`.
    # It must mimic the original `require_role`'s signature (accepting `roles`).
    def mock_require_role_factory(roles: list[str]):
        # This nested function is the actual dependency callable that FastAPI will execute.
        def _mock_user_dependency():
            # Simply return a mock user with the 'Administrator' role.
            return {"username": "test_admin_user", "role": "Administrator", "id": 1}
        return _mock_user_dependency # The factory returns this callable

    # Use patch as a context manager to override `require_role`
    # Patch it at the location it's used in `app.api.user`
    with patch("app.api.user.require_role", side_effect=mock_require_role_factory):
        # We don't need to override get_db here in the fixture
        # because it's patched directly in test_list_users.
        yield # This allows the test to run

    # The patch is automatically cleaned up when exiting the `with` block.