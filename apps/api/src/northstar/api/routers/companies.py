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
    get_company_use_case_provider,
    list_companies_use_case_provider,
)
from northstar.api.schemas.companies import (
    CompanyDetailResponse,
    CompanyListResponse,
    CompanySummaryResponse,
)
from northstar.contexts.companies.application.use_cases import GetCompany, ListCompanies
from northstar.contexts.companies.domain.company import Company
from northstar.contexts.companies.domain.value_objects import CompanyId
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
