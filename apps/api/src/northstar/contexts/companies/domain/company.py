"""The `Company` aggregate root.

Company is the central object of the `companies` context and, over Phase 1+,
of the platform: opportunities (Slice 2), offices/locations (Slice 4), and
company-intelligence facts (Slice 5) all reference or extend it. Slice 1
ships only the fields it actually needs today — extensibility is a structural
property (new optional fields/child value objects can be added in later
slices without touching `CompanyId`, `CompanySlug`, or any field shipped
here), not a speculative schema. See `contexts/companies/CLAUDE.md`.
"""

from __future__ import annotations

from dataclasses import dataclass

from northstar.contexts.companies.domain.value_objects import CompanyId, CompanySlug

_MIN_FOUNDED_YEAR = 1800
_MAX_FOUNDED_YEAR = 2100


@dataclass(frozen=True, slots=True)
class Company:
    """A company on the platform — the aggregate root of this context.

    Every field here is a Slice-1 fact only. Do not add speculative fields
    for future capabilities (culture, reviews, hiring velocity, ESG, …) —
    those arrive additively in the slice that actually needs them.
    """

    id: CompanyId
    slug: CompanySlug
    name: str
    description: str
    industry: str
    website: str
    careers_page_url: str | None = None
    founded_year: int | None = None

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Company.name must not be empty")
        if not self.industry.strip():
            raise ValueError("Company.industry must not be empty")
        if not self.website.strip():
            raise ValueError("Company.website must not be empty")
        if self.founded_year is not None and not (
            _MIN_FOUNDED_YEAR <= self.founded_year <= _MAX_FOUNDED_YEAR
        ):
            raise ValueError(
                f"Company.founded_year {self.founded_year} out of plausible range "
                f"[{_MIN_FOUNDED_YEAR}, {_MAX_FOUNDED_YEAR}]"
            )

    @classmethod
    def create(
        cls,
        *,
        name: str,
        description: str,
        industry: str,
        website: str,
        careers_page_url: str | None = None,
        founded_year: int | None = None,
        slug: CompanySlug | None = None,
    ) -> Company:
        """Construct a new Company, deriving identity and slug if not supplied."""
        return cls(
            id=CompanyId.new(),
            slug=slug or CompanySlug.from_name(name),
            name=name,
            description=description,
            industry=industry,
            website=website,
            careers_page_url=careers_page_url,
            founded_year=founded_year,
        )
