"""`Location` — validated latitude/longitude, nothing more."""

import pytest

from northstar.contexts.geo.domain.value_objects import Location


def test_accepts_valid_coordinates():
    location = Location(latitude=17.4483, longitude=78.3915)
    assert location.latitude == 17.4483
    assert location.longitude == 78.3915


@pytest.mark.parametrize("latitude", [-90.0001, 90.0001, 200])
def test_rejects_out_of_range_latitude(latitude: float):
    with pytest.raises(ValueError):
        Location(latitude=latitude, longitude=0)


@pytest.mark.parametrize("longitude", [-180.0001, 180.0001, 400])
def test_rejects_out_of_range_longitude(longitude: float):
    with pytest.raises(ValueError):
        Location(latitude=0, longitude=longitude)


def test_boundary_values_are_valid():
    Location(latitude=-90, longitude=-180)
    Location(latitude=90, longitude=180)
