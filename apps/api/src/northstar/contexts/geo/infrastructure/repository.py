"""SQLAlchemy implementation of `CompanyLocationRepository`."""

from __future__ import annotations

from geoalchemy2.elements import WKTElement
from geoalchemy2.shape import to_shape
from sqlalchemy.orm import Session

from northstar.contexts.companies.contract import CompanyId
from northstar.contexts.geo.domain.value_objects import Location
from northstar.contexts.geo.infrastructure.models import CompanyLocationModel


def _to_wkt(location: Location) -> WKTElement:
    return WKTElement(f"POINT({location.longitude} {location.latitude})", srid=4326)


def _to_domain(row: CompanyLocationModel) -> Location:
    point = to_shape(row.location)
    return Location(latitude=point.y, longitude=point.x)


class SqlAlchemyCompanyLocationRepository:
    """Postgres+PostGIS-backed `CompanyLocationRepository`."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_company_id(self, company_id: CompanyId) -> Location | None:
        row = self._session.get(CompanyLocationModel, company_id.value)
        return _to_domain(row) if row is not None else None

    def set_for_company(self, company_id: CompanyId, location: Location) -> None:
        row = self._session.get(CompanyLocationModel, company_id.value)
        if row is None:
            row = CompanyLocationModel(
                company_id=company_id.value, location=_to_wkt(location)
            )
            self._session.add(row)
        else:
            row.location = _to_wkt(location)
