"""tests for routes accessible with and without authentication"""
import pytest
from fastapi import status

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "user_count", [1, 50], ids=["single user", "multiple users"]
)
async def test_user_can_signup(client, user_count, user_factory):
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


@pytest.mark.parametrize("users", [10], indirect=True)
async def test_get_users(client, users):  # pylint:disable=unused-argument
    """validates that users detail can be retrived with a get request"""
    # Arrange: create users in database
    # handled by 'users' fixture with indirect parametrization

    # Act: send get request to the endpoint
    response = await client.get("api/v1/users", follow_redirects=True)

    # Assert: users data is received in the response
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 10


@pytest.mark.parametrize("users", [50], indirect=True)
async def test_get_users_pagination(
    client, users
):  # pylint:disable=unused-argument
    """validates that users detail can be retrived with a get request"""
    # Arrange: create users in database
    # handled by 'users' fixture with indirect parametrization

    # Act: send get request to the endpoint
    for skip in range(0, 50, 10):
        response = await client.get(
            f"api/v1/users?skip={skip}&limit=10", follow_redirects=True
        )

        # Assert: users data is received in the response
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 10


async def test_update_user(client, users, location_factory):
    """validates that an existing user can be updated"""
    # Arrange: create a user in database
    # handeled by users fixture
    user_id = users[0].id

    # Act: update user location
    new_location = location_factory(coordinates=[28.321, 72.321])
    response = await client.patch(
        f"/api/v1/users/{users[0].id}",
        json={"location": new_location.dict()},
        follow_redirects=True,
    )

    # Assert: request is processed
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # Assert user location is updated
    response = await client.get(f"/api/v1/users/{user_id}")
    assert (
        response.json()["location"]["coordinates"] == new_location.coordinates
    )


async def test_user_delete(client, users):
    """validates that an existing user can be deleted"""
    # Arrange: create a user in database
    # handeled by users fixture
    user_id = users[0].id

    # Act: delete user
    response = await client.delete(f"/api/v1/users/{user_id}")

    # Assert: response code
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # Assert: user is deleted
    response = await client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
