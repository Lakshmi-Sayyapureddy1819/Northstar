"""Companies router — Slice 1 (Company Foundation).

Thin HTTP layer: parses/validates the request, calls the application layer's
use cases, converts the result to a response schema. No business logic here
(blueprint §3.3 — Router → Application → Domain).
"""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from northstar.api.dependencies import (
    find_nearby_companies_use_case_provider,
    get_company_by_slug_use_case_provider,
    get_company_use_case_provider,
    list_companies_use_case_provider,
)
from northstar.api.schemas.companies import (
    CompanyDetailResponse,
    CompanyListResponse,
    CompanySummaryResponse,
    NearbyCompanyListResponse,
    NearbyCompanyResponse,
)
from northstar.contexts.companies.application.use_cases import (
    GetCompany,
    GetCompanyBySlug,
    ListCompanies,
)
from northstar.contexts.companies.domain.company import Company
from northstar.contexts.companies.domain.value_objects import CompanyId, CompanySlug
from northstar.contexts.geo.application.use_cases import FindNearbyCompanies
from northstar.contexts.geo.contract import Location, NearbyQuery
from northstar.shared_kernel import Err, Ok

router = APIRouter(prefix="/companies", tags=["companies"])


def _to_summary_response(company: Company) -> CompanySummaryResponse:
    return CompanySummaryResponse(
        id=str(company.id),
        slug=str(company.slug),
        name=company.name,
        industry=company.industry,
        description=company.description,
    )


def _to_detail_response(company: Company) -> CompanyDetailResponse:
    return CompanyDetailResponse(
        id=str(company.id),
        slug=str(company.slug),
        name=company.name,
        description=company.description,
        industry=company.industry,
        website=company.website,
        careers_page_url=company.careers_page_url,
        founded_year=company.founded_year,
    )


@router.get("", response_model=CompanyListResponse, summary="List companies")
def list_companies(
    use_case: Annotated[ListCompanies, Depends(list_companies_use_case_provider)],
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> CompanyListResponse:
    result = use_case.execute(limit=limit, offset=offset)
    match result:
        case Ok(companies):
            return CompanyListResponse(
                items=[_to_summary_response(c) for c in companies],
                limit=limit,
                offset=offset,
            )
        case Err(error):
            raise HTTPException(status_code=400, detail=error.message)


@router.get(
    "/nearby", response_model=NearbyCompanyListResponse, summary="Find nearby companies"
)
def nearby_companies(
    nearby_use_case: Annotated[
        FindNearbyCompanies, Depends(find_nearby_companies_use_case_provider)
    ],
    get_company_use_case: Annotated[GetCompany, Depends(get_company_use_case_provider)],
    lat: Annotated[float, Query(ge=-90, le=90)],
    lng: Annotated[float, Query(ge=-180, le=180)],
    radius_km: Annotated[float, Query(gt=0, le=100)] = 10.0,
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> NearbyCompanyListResponse:
    # This route must be registered before "/{company_id}" — otherwise
    # "/companies/nearby" would match that pattern first (company_id="nearby")
    # and fail UUID parsing instead of reaching this handler.
    query = NearbyQuery(
        origin=Location(latitude=lat, longitude=lng), radius_km=radius_km
    )
    nearby_result = nearby_use_case.execute(query, limit=limit, offset=offset)
    match nearby_result:
        case Ok(nearby):
            items: list[NearbyCompanyResponse] = []
            for result in nearby:
                company_result = get_company_use_case.execute(result.company_id)
                match company_result:
                    case Ok(company):
                        items.append(
                            NearbyCompanyResponse(
                                **_to_summary_response(company).model_dump(),
                                latitude=result.location.latitude,
                                longitude=result.location.longitude,
                                distance_km=round(result.distance_km, 2),
                            )
                        )
                    case Err(_):
                        # location exists but company vanished — skip, don't 500
                        continue
            return NearbyCompanyListResponse(items=items, limit=limit, offset=offset)
        case Err(error):
            raise HTTPException(status_code=400, detail=error.message)


@router.get(
    "/by-slug/{slug}",
    response_model=CompanyDetailResponse,
    summary="Get company detail by slug (deep-linkable route)",
)
def get_company_by_slug(
    slug: str,
    use_case: Annotated[
        GetCompanyBySlug, Depends(get_company_by_slug_use_case_provider)
    ],
) -> CompanyDetailResponse:
    try:
        company_slug = CompanySlug(slug)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    result = use_case.execute(company_slug)
    match result:
        case Ok(company):
            return _to_detail_response(company)
        case Err(error):
            raise HTTPException(status_code=404, detail=error.message)


@router.get(
    "/{company_id}", response_model=CompanyDetailResponse, summary="Get company detail"
)
def get_company(
    company_id: uuid.UUID,
    use_case: Annotated[GetCompany, Depends(get_company_use_case_provider)],
) -> CompanyDetailResponse:
    result = use_case.execute(CompanyId(company_id))
    match result:
        case Ok(company):
            return _to_detail_response(company)
        case Err(error):
            raise HTTPException(status_code=404, detail=error.message)
