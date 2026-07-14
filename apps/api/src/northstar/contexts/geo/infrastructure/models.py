"""SQLAlchemy mapping for a company's location.

One row per company for MVP (primary key = `company_id`) — multiple offices
per company is an additive extension for later, not modeled here (see
`docs/features/phase1/slice-2-seed-hyderabad-dataset.md`).
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from geoalchemy2 import Geography
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from northstar.platform.db import Base


class CompanyLocationModel(Base):
    """The `company_locations` table."""

    __tablename__ = "company_locations"

    company_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("companies.id"), primary_key=True
    )
    # geoalchemy2 accepts a WKTElement on write and returns a WKBElement on
    # read — no single Mapped[...] type describes both sides precisely.
    location: Mapped[Any] = mapped_column(
        Geography(geometry_type="POINT", srid=4326, spatial_index=True),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
