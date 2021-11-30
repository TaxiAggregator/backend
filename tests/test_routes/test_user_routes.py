"""tests for users routes"""
from typing import List

import pytest
from fastapi import status
from httpx import AsyncClient
from server.models import User
from tests.factories import LocationFactory, UserFactory

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "user_count", [1, 50], ids=["single user", "multiple users"]
)
async def test_user_can_signup(
    client: AsyncClient, user_count: int, user_factory: UserFactory
):
    """validates that a new user can signup"""
    # Arrange: create user data
    users = user_factory.create_batch(user_count)
    user_dicts = [user.dict() for user in users]

    # Act: post user data to the endpoint
    response = await client.post(
        "/api/v1/users", json=user_dicts, follow_redirects=True
    )

    # Assert: user is created in database
    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.json()) == user_count


@pytest.mark.parametrize(
    "users", [10, 0], indirect=True, ids=["users exist", "users don't exist"]
)
async def test_get_users(client: AsyncClient, users: List[User]):
    """validates that users detail can be retrived with a get request"""
    # Arrange: create users in database
    # handled by 'users' fixture with indirect parametrization

    # Act: send get request to the endpoint
    response = await client.get("api/v1/users", follow_redirects=True)

    # Assert: users data is received in the response
    expected_status_code = (
        status.HTTP_200_OK if users else status.HTTP_404_NOT_FOUND
    )
    assert response.status_code == expected_status_code
    if users:
        assert len(response.json()) == len(users)


@pytest.mark.parametrize("users", [50], indirect=True)
async def test_get_users_pagination(client: AsyncClient, users: List[User]):
    """validates that users detail can be retrived with a get request"""
    total_users = 0
    limit = 10

    # Arrange: create users in database
    # handled by 'users' fixture with indirect parametrization

    # Act: send get request to the endpoint
    for skip in range(0, len(users), limit):
        response = await client.get(
            f"api/v1/users?skip={skip}&limit={limit}", follow_redirects=True
        )

        # Assert: users data is received in the response
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == limit

        total_users += len(response.json())

    # Assert all 50 users are retrieved
    assert total_users == len(users)


@pytest.mark.parametrize(
    "valid", [True, False], ids=["user exists", "user doesn't exist"]
)
async def test_get_user_by_id(
    client: AsyncClient, users: List[User], valid: bool
):
    """validate that user details can be retrieved by user id"""
    # Arrange: create a user in database
    # handled by 'users' fixture
    user_id = str(users[0].id) if valid else "5eb7cf5a86d9755df3a6c593"

    # Act: send get request to the endpoint
    response = await client.get(f"/api/v1/users/{user_id}")

    # Assert: user details are retrieved
    expected_status_code = (
        status.HTTP_200_OK if valid else status.HTTP_404_NOT_FOUND
    )
    assert response.status_code == expected_status_code
    if valid:
        assert user_id == response.json()["_id"]


@pytest.mark.parametrize(
    "valid", [True, False], ids=["user exists", "user doesn't exist"]
)
async def test_update_user(
    client: AsyncClient,
    users: List[User],
    location_factory: LocationFactory,
    valid: bool,
):
    """validates that an existing user can be updated"""
    # Arrange: create a user in database
    # handeled by users fixture
    user_id = str(users[0].id) if valid else "5eb7cf5a86d9755df3a6c593"

    # Act: update user location
    new_location = location_factory(coordinates=[28.321, 72.321])  # type: ignore
    response = await client.patch(
        f"/api/v1/users/{user_id}",
        json={"location": new_location.dict()},
        follow_redirects=True,
    )

    # Assert: request is processed
    expected_status_code = (
        status.HTTP_204_NO_CONTENT if valid else status.HTTP_404_NOT_FOUND
    )
    assert response.status_code == expected_status_code
    # Assert: user location is updated
    if valid:
        response = await client.get(f"/api/v1/users/{user_id}")
        assert (
            response.json()["location"]["coordinates"]
            == new_location.coordinates
        )


@pytest.mark.parametrize(
    "valid", [True, False], ids=["user exists", "user doesn't exist"]
)
async def test_user_delete(
    client: AsyncClient, users: List[User], valid: bool
):
    """validates that an existing user can be deleted"""
    # Arrange: create a user in database
    # handeled by users fixture
    user_id = str(users[0].id) if valid else "5eb7cf5a86d9755df3a6c593"

    # Act: delete user
    response = await client.delete(f"/api/v1/users/{user_id}")

    # Assert: response code
    expected_status_code = (
        status.HTTP_204_NO_CONTENT if valid else status.HTTP_404_NOT_FOUND
    )
    assert response.status_code == expected_status_code
    # Assert: user is deleted
    if valid:
        response = await client.get(f"/api/v1/users/{user_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
