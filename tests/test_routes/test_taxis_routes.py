"""tests for taxis routes"""
from typing import List

import pytest
from fastapi import status
from httpx import AsyncClient
from server.models import Taxi
from tests.factories import LocationFactory, TaxiFactory

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "taxi_count", [1, 50], ids=["single taxi", "multiple taxi"]
)
async def test_taxi_can_be_registered(
    client: AsyncClient, taxi_count: int, taxi_factory: TaxiFactory
):
    """validates that new taxi(s) can be registered"""
    # Arrange: create taxi data
    taxis = taxi_factory.create_batch(taxi_count)
    taxi_dicts = [taxi.dict() for taxi in taxis]

    # Act: post taxi data to the endpoint
    response = await client.post(
        "/api/v1/taxis", json=taxi_dicts, follow_redirects=True
    )

    # Assert: taxi is created
    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.json()) == taxi_count


@pytest.mark.parametrize("taxis", [10], indirect=True)
async def test_get_taxis(client: AsyncClient, taxis: List[Taxi]):
    """validates that taxi details can be retrived with a get request"""
    # Arrange: create taxis in database
    # handled by 'taxis' fixture with indirect parametrization

    # Act: send get request to endpoint
    response = await client.get("/api/v1/taxis", follow_redirects=True)

    # Assert: taxis data is received in the response
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(taxis)


@pytest.mark.parametrize("taxis", [50], indirect=True)
async def test_get_taxis_pagination(client: AsyncClient, taxis: List[Taxi]):
    """validates that taxis detail can be retrived with a get request"""
    total_taxis = 0
    limit = 10

    # Arrange: create taxis in database
    # handled by 'taxis' fixture with indirect parametrization

    # Act: send get request to the endpoint
    for skip in range(0, len(taxis), limit):
        response = await client.get(
            f"api/v1/taxis?skip={skip}&limit={limit}", follow_redirects=True
        )

        # Assert: taxis data is received in the response
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == limit

        total_taxis += len(response.json())

    # Assert: all 50 taxis are retrieved
    assert total_taxis == len(taxis)


async def test_get_taxis_with_no_taxis_in_database(client: AsyncClient):
    """validates that correct error code for response if no taxis in database"""
    # Arrange: no taxis in taxi collection
    # all collections are cleaned before each test

    # Act: send get request to the endpoint
    response = await client.get("/api/v1/taxis", follow_redirects=True)

    # Assert: response is Not Found
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "valid", [True, False], ids=["taxi exist", "taxi doesn't exist"]
)
async def test_get_taxi_by_id(
    client: AsyncClient, taxis: List[Taxi], valid: bool
):
    """validates that a taxi can be retrieved by id"""
    # Arrange: create a taxi in database
    # handled by 'taxis' fixture
    taxi_id = str(taxis[0].id) if valid else "5eb7cf5a86d9755df3a6c593"

    # Act: send get request to the endpoint
    response = await client.get(f"/api/v1/taxis/{taxi_id}")

    # Assert: taxi details are retrieved
    expected_status_code = (
        status.HTTP_200_OK if valid else status.HTTP_404_NOT_FOUND
    )
    assert response.status_code == expected_status_code
    if valid:
        assert taxi_id == response.json()["_id"]


@pytest.mark.parametrize(
    "valid", [True, False], ids=["taxi exist", "taxi doesn't exist"]
)
async def test_update_taxi(
    client: AsyncClient,
    location_factory: LocationFactory,
    taxis: List[Taxi],
    valid: bool,
):
    """validates that taxi details can be updated"""
    # Arrange: create a taxi in database
    # handled by 'taxis' fixture
    taxi_id = str(taxis[0].id) if valid else "5eb7cf5a86d9755df3a6c593"

    # Act: send patch request to the endpoint
    new_location = location_factory(coordinates=[28.321, 72.321])  # type: ignore
    response = await client.patch(
        f"/api/v1/taxis/{taxi_id}",
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
        response = await client.get(f"/api/v1/taxis/{taxi_id}")
        assert (
            response.json()["location"]["coordinates"]
            == new_location.coordinates
        )


@pytest.mark.parametrize(
    "valid", [True, False], ids=["taxi exist", "taxi doesn't exist"]
)
async def test_delete_taxi(
    client: AsyncClient, taxis: List[Taxi], valid: bool
):
    """validates that a taxi can be deleted"""
    # Arrange: create a taxi in database
    # handled by 'taxis' fixture

    # Act: send a delete request to the endpoint
    taxi_id = str(taxis[0].id) if valid else "5eb7cf5a86d9755df3a6c593"
    response = await client.delete(
        f"/api/v1/taxis/{taxi_id}", follow_redirects=True
    )

    # Assert: request is processed
    expected_status_code = (
        status.HTTP_204_NO_CONTENT if valid else status.HTTP_404_NOT_FOUND
    )
    assert response.status_code == expected_status_code
    # Assert: taxi is deleted
    if valid:
        response = await client.get(f"/api/v1/taxis/{taxi_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "taxis", [5, 0], ids=["taxis exist", "taxis don't exist"], indirect=True
)
async def test_fetch_taxis_within_radius(
    client: AsyncClient, taxis: List[Taxi]
):
    """validates that /near query works"""
    # Arrange: create taxis in database
    # handled by 'taxis' fixture with indirect parametrization

    # Act: query for taxis
    params = {
        "longitude": taxis and taxis[0].location.coordinates[0] or 72.123,
        "latitude": taxis and taxis[0].location.coordinates[1] or 12.123,
        "max_distance": 100,
    }
    response = await client.get(
        "/api/v1/taxis/near", params=params, follow_redirects=True
    )

    # Assert: list of taxis is returned
    expected_status_code = (
        status.HTTP_200_OK if taxis else status.HTTP_404_NOT_FOUND
    )
    assert response.status_code == expected_status_code
    if taxis:
        assert len(response.json()) > 0


@pytest.mark.parametrize(
    "taxis", [5, 0], ids=["taxis exist", "taxis don't exist"], indirect=True
)
async def test_fetch_nearest_taxis(client: AsyncClient, taxis: List[Taxi]):
    """validates that /nearest query works"""
    # Arrange: create taxis in database
    # handled by 'taxis' fixture with indirect parametrization

    # Act: query for taxis
    params = {
        "longitude": 28.1213,
        "latitude": 72.123,
    }
    response = await client.get(
        "/api/v1/taxis/nearest", params=params, follow_redirects=True
    )

    # Assert: list of taxis is returned
    expected_status_code = (
        status.HTTP_200_OK if taxis else status.HTTP_404_NOT_FOUND
    )
    assert response.status_code == expected_status_code
    if taxis:
        assert len(response.json()) == len(taxis)
