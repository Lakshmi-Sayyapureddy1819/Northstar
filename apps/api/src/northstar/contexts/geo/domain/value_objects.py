"""Value objects for the `geo` domain.

`Location` is the first-class geographic concept every other context (and
Slice 3's map query) depends on — never raw latitude/longitude floats passed
around ad hoc. Validated at construction, same pattern as `companies`'
`CompanyId`/`CompanySlug` (`contexts/companies/domain/value_objects.py`).
"""

from __future__ import annotations

from dataclasses import dataclass

_MIN_LATITUDE, _MAX_LATITUDE = -90.0, 90.0
_MIN_LONGITUDE, _MAX_LONGITUDE = -180.0, 180.0


@dataclass(frozen=True, slots=True)
class Location:
    """A validated geographic point (WGS84 latitude/longitude)."""

    latitude: float
    longitude: float

    def __post_init__(self) -> None:
        if not (_MIN_LATITUDE <= self.latitude <= _MAX_LATITUDE):
            raise ValueError(
                f"Location.latitude {self.latitude} out of range "
                f"[{_MIN_LATITUDE}, {_MAX_LATITUDE}]"
            )
        if not (_MIN_LONGITUDE <= self.longitude <= _MAX_LONGITUDE):
            raise ValueError(
                f"Location.longitude {self.longitude} out of range "
                f"[{_MIN_LONGITUDE}, {_MAX_LONGITUDE}]"
            )
