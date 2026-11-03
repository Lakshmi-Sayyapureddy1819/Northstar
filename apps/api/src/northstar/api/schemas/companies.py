"""HTTP response schemas for the companies router.

These mirror `companies.contract`'s read-model shapes but are the API
layer's own Pydantic models — the thin HTTP layer owns its wire format, and
this is also what FastAPI serializes into the OpenAPI schema (ADR 0008).
"""

from __future__ import annotations

from pydantic import BaseModel


class CompanySummaryResponse(BaseModel):
    """Card-sized company shape."""

    id: str
    slug: str
    name: str
    industry: str
    description: str


class CompanyDetailResponse(BaseModel):
    """Full company profile shape."""

    id: str
    slug: str
    name: str
    description: str
    industry: str
    website: str
    careers_page_url: str | None
    founded_year: int | None


class CompanyListResponse(BaseModel):
    """A page of company summaries."""

    items: list[CompanySummaryResponse]
    limit: int
    offset: int


class NearbyCompanyResponse(CompanySummaryResponse):
    """A company summary plus its coordinates and distance from the search
    origin — the map needs real coordinates to place a marker."""

    latitude: float
    longitude: float
    distance_km: float


class NearbyCompanyListResponse(BaseModel):
    """A page of nearby-company results, ordered by distance."""

    items: list[NearbyCompanyResponse]
    limit: int
    offset: int
