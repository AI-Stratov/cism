from http import HTTPStatus

import pytest
from httpx import AsyncClient

from src.main import app


@pytest.mark.asyncio
async def test_smoke_test():
    """
    Smoke test to check if the application is running and returns the expected
    redirect response.
    """
    async with AsyncClient(app=app) as client:
        response = await client.get("http://127.0.0.1:8000/")

    assert (
        response.status_code == HTTPStatus.TEMPORARY_REDIRECT
    ), f"Unexpected status code: {response.status_code}"


@pytest.mark.asyncio
async def test_register_user(request_payload):
    """
    Test case to register a user.
    """
    async with AsyncClient(app=app) as client:
        response = await client.post(
            "http://127.0.0.1:8000/auth/register", json=request_payload,
        )

    assert (
        response.status_code == HTTPStatus.OK
    ), f"Failed to register user: {response.text}"
    response_data = response.json()
    assert (
        response_data["message"]
        == f"User {request_payload['username']} registered successfully"
    )
    assert response_data["username"] == request_payload["username"]


@pytest.mark.asyncio
async def test_login_user(request_payload):
    """
    Test case to login a user.
    """
    async with AsyncClient(app=app) as client:
        response = await client.post(
            "http://127.0.0.1:8000/auth/login", json=request_payload,
        )

    assert (
        response.status_code == HTTPStatus.OK
    ), f"Failed to login user: {response.text}"
    response_data = response.json()
    assert "message" in response_data
    assert "token" in response_data


@pytest.mark.asyncio
async def test_get_users_unauthorized():
    """
    Test case to get the list of users without authorization.
    """
    async with AsyncClient(app=app) as client:
        response = await client.get("http://127.0.0.1:8000/auth/users")

    assert (
        response.status_code == HTTPStatus.FORBIDDEN
    ), "Unauthorized user should not be able to get the list of users"


@pytest.mark.asyncio
async def test_get_users_authorized(request_payload):
    """
    Test case to get the list of users with authorization.
    """
    async with AsyncClient(app=app) as client:
        response = await client.post(
            "http://127.0.0.1:8000/auth/login", json=request_payload,
        )

    assert response.status_code == HTTPStatus.OK, "Login should have succeeded"

    response_data = response.json()
    assert (
        "token" in response_data
    ), "Access token should be present in the login response"

    access_token = response_data["token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    async with AsyncClient(app=app) as client:
        response = await client.get(
            "http://127.0.0.1:8000/auth/users", headers=headers,
        )

    assert (
        response.status_code == HTTPStatus.OK
    ), "Authorized user should be able to get the list of users"
    users = response.json()
    assert isinstance(users, list), "Response data is not a list"
    assert any(
        user.get("username") == request_payload.get("username")
        for user in users
    )


@pytest.mark.asyncio
async def test_register_user_existing_username(request_payload):
    """
    Test case to register a user with an existing username.
    """
    async with AsyncClient(app=app) as client:
        response = await client.post(
            "http://127.0.0.1:8000/auth/register", json=request_payload,
        )

    assert (
        response.status_code == HTTPStatus.BAD_REQUEST
    ), "User with the same username was registered again"


@pytest.mark.asyncio
async def test_register_user_validation_error(bad_payload):
    """
    Test case to register a user with
    invalid payload causing a validation error.
    """
    async with AsyncClient(app=app) as client:
        response = await client.post(
            "http://127.0.0.1:8000/auth/register",
            json=bad_payload,
        )

    assert (
        response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    ), "User registration should have failed due to validation error"


@pytest.mark.asyncio
async def test_login_user_nonexistent_user(nonexisting_user_payload):
    """
    Test case to login a non-existing user.
    """
    async with AsyncClient(app=app) as client:
        response = await client.post(
            "http://127.0.0.1:8000/auth/login",
            json=nonexisting_user_payload,
        )

    assert (
        response.status_code == HTTPStatus.UNAUTHORIZED
    ), "Login should have failed for nonexistent user"
