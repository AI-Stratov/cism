from http import HTTPStatus

import pytest
from httpx import AsyncClient

from src.main import app
from src.tasks.schemas import TaskStatus


@pytest.mark.asyncio
async def test_create_task_low_priority():
    """
    Test case to create a low priority task.
    """
    async with AsyncClient(app=app) as client:
        response = await client.post(
            "http://127.0.0.1:8000/tasks/create/?priority=low_priority_queue",
        )

    assert (
        response.status_code == HTTPStatus.OK
    ), f"Failed to create low priority task: {response.text}"
    task = response.json()
    assert "id" in task
    assert task["status"] == TaskStatus.CREATED


@pytest.mark.asyncio
async def test_create_task_high_priority():
    """
    Test case to create a high priority task.
    """
    async with AsyncClient(app=app) as client:
        response = await client.post(
            "http://127.0.0.1:8000/tasks/create/?priority=high_priority_queue",
        )

    assert (
        response.status_code == HTTPStatus.OK
    ), f"Failed to create high priority task: {response.text}"
    task = response.json()
    assert "id" in task
    assert task["status"] == TaskStatus.CREATED


@pytest.mark.asyncio
async def test_get_existing_task():
    """
    Test case to get the status of an existing task.
    """
    async with AsyncClient(app=app) as client:
        response = await client.post(
            "http://127.0.0.1:8000/tasks/create/?priority=low_priority_queue",
        )
    assert (
        response.status_code == HTTPStatus.OK
    ), f"Failed to create task: {response.text}"
    task = response.json()
    task_id = task["id"]
    async with AsyncClient(app=app) as client:
        response = await client.get(
            f"http://127.0.0.1:8000/tasks/status/{task_id}/",
        )

    assert (
        response.status_code == HTTPStatus.OK
    ), f"Failed to retrieve task: {response.text}"
    task_response = response.json()
    assert "id" in task_response
    assert task_response["id"] == task_id
    assert task_response["status"] == TaskStatus.CREATED


@pytest.mark.asyncio
async def test_get_nonexistent_task():
    """
    Test case to get the status of a nonexistent task.
    """
    task_id = 99999

    async with AsyncClient(app=app) as client:
        response = await client.get(
            f"http://127.0.0.1:8000/tasks/status/{task_id}/",
        )

    assert (
        response.status_code == HTTPStatus.NOT_FOUND
    ), f"Expected 404 response, got: {response.status_code}"
