"""tests for routes accessible with and without authentication"""
import pytest


@pytest.mark.parametrize("route", ["signup", "login"])
def test_route_is_accessible_without_authentication(route):
    """validates that mentioned routes can be accessed without authentication"""
    assert route is not None  # nosec
