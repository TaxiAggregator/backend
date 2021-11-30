"""Pytest fixtures"""
from typing import List

import pytest
from asgi_lifespan import LifespanManager
from beanie.operators import In
from fastapi import FastAPI
from httpx import AsyncClient
from pytest_factoryboy import register
from server.main import app
from server.models import Taxi, User

from tests.factories import LocationFactory, TaxiFactory, UserFactory

register(LocationFactory)
register(TaxiFactory)
register(UserFactory)


async def clear_database(server: FastAPI) -> None:
    """Empties the test database"""
    for collection in await server.db.list_collections():  # type: ignore
        await server.db[collection["name"]].delete_many({})  # type: ignore


@pytest.fixture
async def client():
    """Async server client that handles lifespan and teardown"""
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as _client:
            try:
                yield _client
            except Exception as exc:  # pylint: disable=broad-except
                print(exc)
            finally:
                await clear_database(app)


@pytest.fixture
async def users(request, user_factory) -> List[User]:
    """create user(s)"""
    # number of users to be created (provided by test using indrect parametrization)
    count = request.param if hasattr(request, "param") else 1

    # if 0 users are to be created, return an empty list
    if not count:
        return []

    created_users = user_factory.create_batch(count)
    result = await User.insert_many(created_users)
    ids = result.inserted_ids

    # need to extract users from database as factory do not save them in database
    return await User.find_many(In(User.id, ids)).to_list()


@pytest.fixture
async def taxis(request, taxi_factory) -> List[Taxi]:
    """create user(s)"""
    # number of taxis to be created (provided by test using indrect parametrization)
    count = request.param if hasattr(request, "param") else 1

    # if 0 taxis are to be created, return an empty list
    if not count:
        return []

    created_taxis = taxi_factory.create_batch(count)
    result = await Taxi.insert_many(created_taxis)
    ids = result.inserted_ids

    # need to extract taxis from database as factory do not save them in database
    return await Taxi.find_many(In(Taxi.id, ids)).to_list()
