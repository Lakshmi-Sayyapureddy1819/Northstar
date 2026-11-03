"""SQLAlchemy implementation of `CompanyLocationRepository`."""

from __future__ import annotations

from geoalchemy2.elements import WKBElement, WKTElement
from geoalchemy2.functions import ST_Distance, ST_DWithin
from geoalchemy2.shape import to_shape
from sqlalchemy import select
from sqlalchemy.orm import Session

from northstar.contexts.companies.contract import CompanyId
from northstar.contexts.geo.contract import NearbyQuery, NearbyResult
from northstar.contexts.geo.domain.value_objects import Location
from northstar.contexts.geo.infrastructure.models import CompanyLocationModel


def _to_wkt(location: Location) -> WKTElement:
    return WKTElement(f"POINT({location.longitude} {location.latitude})", srid=4326)


def _to_domain_point(geometry: WKBElement | WKTElement) -> Location:
    point = to_shape(geometry)
    return Location(latitude=point.y, longitude=point.x)


class SqlAlchemyCompanyLocationRepository:
    """Postgres+PostGIS-backed `CompanyLocationRepository`."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_company_id(self, company_id: CompanyId) -> Location | None:
        row = self._session.get(CompanyLocationModel, company_id.value)
        return _to_domain_point(row.location) if row is not None else None

    def set_for_company(self, company_id: CompanyId, location: Location) -> None:
        row = self._session.get(CompanyLocationModel, company_id.value)
        if row is None:
            row = CompanyLocationModel(
                company_id=company_id.value, location=_to_wkt(location)
            )
            self._session.add(row)
        else:
            row.location = _to_wkt(location)

    def find_nearby(
        self, query: NearbyQuery, *, limit: int = 50, offset: int = 0
    ) -> list[NearbyResult]:
        origin = _to_wkt(query.origin)
        radius_m = query.radius_km * 1000
        distance_m = ST_Distance(CompanyLocationModel.location, origin).label(
            "distance_m"
        )
        stmt = (
            select(
                CompanyLocationModel.company_id,
                CompanyLocationModel.location,
                distance_m,
            )
            .where(ST_DWithin(CompanyLocationModel.location, origin, radius_m))
            .order_by(distance_m)
            .limit(limit)
            .offset(offset)
        )
        rows = self._session.execute(stmt).all()
        return [
            NearbyResult(
                company_id=CompanyId(row.company_id),
                location=_to_domain_point(row.location),
                distance_km=row.distance_m / 1000,
            )
            for row in rows
        ]
