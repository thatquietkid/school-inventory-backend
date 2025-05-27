from fastapi import HTTPException, status
from unittest.mock import MagicMock, patch
from app.api.auth import register_user
from app.schemas.user import UserCreate
from app.models import user as user_model
import pytest
from fastapi import HTTPException
from app.api.auth import login

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def user_data():
    return UserCreate(
        username="testuser",
        full_name="Test User",
        password="password123",
        role="Student"
    )

def test_register_user_success(mock_db, user_data):
    # Simulate no existing user
    mock_db.query().filter_by().first.return_value = None
    # Simulate user model
    with patch("app.api.auth.hash_password", return_value="hashed_pw"):
        mock_user = MagicMock(spec=user_model.User)
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None
        with patch("app.models.user.User", return_value=mock_user):
            result = register_user(user_data, db=mock_db)
            assert result == mock_user
            mock_db.add.assert_called_once()
            mock_db.commit.assert_called_once()
            mock_db.refresh.assert_called_once_with(mock_user)

def test_register_user_existing_username(mock_db, user_data):
    # Simulate existing user
    mock_db.query().filter_by().first.return_value = MagicMock()
    with pytest.raises(HTTPException) as exc:
        register_user(user_data, db=mock_db)
    assert exc.value.status_code == 400
    assert exc.value.detail == "Username already exists"

def test_register_user_admin_role_forbidden(mock_db):
    user = UserCreate(
        username="adminuser",
        full_name="Admin User",
        password="adminpass",
        role="Administrator"
    )
    with pytest.raises(HTTPException) as exc:
        register_user(user, db=mock_db)
    assert exc.value.status_code == status.HTTP_403_FORBIDDEN
    assert exc.value.detail == "Registration with Administrator role is not allowed."
    class DummyFormData:
        def __init__(self, username, password):
            self.username = username
            self.password = password

    @pytest.fixture
    def mock_db():
        return MagicMock()

    @pytest.fixture
    def user_obj():
        user = MagicMock()
        user.username = "testuser"
        user.password = "hashed_pw"
        user.role = "Student"
        return user

    def test_login_success(mock_db, user_obj):
        form_data = DummyFormData("testuser", "password123")
        with patch("app.api.auth.get_user_by_username", return_value=user_obj), \
             patch("app.api.auth.pwd_context.verify", return_value=True), \
             patch("app.api.auth.create_access_token", return_value="token123"):
            result = login(form_data=form_data, db=mock_db)
            assert result == {"access_token": "token123", "token_type": "bearer"}

    def test_login_user_not_found(mock_db):
        form_data = DummyFormData("nouser", "password123")
        with patch("app.api.auth.get_user_by_username", return_value=None):
            with pytest.raises(HTTPException) as exc:
                login(form_data=form_data, db=mock_db)
            assert exc.value.status_code == 400
            assert exc.value.detail == "Incorrect username or password"

    def test_login_wrong_password(mock_db, user_obj):
        form_data = DummyFormData("testuser", "wrongpassword")
        with patch("app.api.auth.get_user_by_username", return_value=user_obj), \
             patch("app.api.auth.pwd_context.verify", return_value=False):
            with pytest.raises(HTTPException) as exc:
                login(form_data=form_data, db=mock_db)
            assert exc.value.status_code == 400
            assert exc.value.detail == "Incorrect username or password"
