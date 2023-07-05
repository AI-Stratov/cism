import pytest

from src.database import get_db
from src.models import User


@pytest.fixture(scope="session")
def request_payload() -> dict:
    """
    Fixture providing a valid request payload for testing.
    """
    return {
        "username": "testuser99",
        "password": "testuser99",
    }


@pytest.fixture(scope="session")
def bad_payload() -> dict:
    """
    Fixture providing a bad (invalid) request payload for testing.
    """
    return {
        "username": "testusertestuser",
        "password": "pass",
    }


@pytest.fixture(scope="session")
def nonexisting_user_payload() -> dict:
    """
    Fixture providing a request payload for a non-existing user for testing.
    """
    return {
        "username": "nonexistentuser",
        "password": "password123",
    }


@pytest.fixture(scope="session", autouse=True)
def cleanup_created_records(
    request, request_payload, bad_payload, nonexisting_user_payload,
):
    """
    Fixture for cleaning up created records after testing.

    This fixture is responsible for cleaning up the records created during
    testing, ensuring a clean state for subsequent tests.

    Args:
        request: pytest request object
        request_payload: Valid request payload
        bad_payload: Invalid request payload
        nonexisting_user_payload: Request payload for a non-existing user
    """

    def cleanup():
        db_generator = get_db()
        db = next(db_generator)
        try:
            username = request_payload.get("username")
            user = db.query(User).filter(User.username == username).first()
            if user:
                db.delete(user)
                db.commit()
            username = bad_payload.get("username")
            user = db.query(User).filter(User.username == username).first()
            if user:
                db.delete(user)
                db.commit()
            username = nonexisting_user_payload.get("username")
            user = db.query(User).filter(User.username == username).first()
            if user:
                db.delete(user)
                db.commit()
        finally:
            db.close()

    request.addfinalizer(cleanup)
