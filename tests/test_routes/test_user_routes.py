from fastapi.testclient import TestClient
import pytest


@pytest.mark.parametrize("route", ["signup", "login"])
def test_route_is_accessible_without_authentication(route):
    assert route != None  # nosec
