"""SQLAlchemy mapping for `Company`. Infrastructure only — the domain entity
above never imports this module (Clean Architecture: dependencies point
inward, enforced by import-linter's layering contract).
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from northstar.platform.db import Base


class CompanyModel(Base):
    """The `companies` table."""

    __tablename__ = "companies"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String)
    industry: Mapped[str] = mapped_column(String(255))
    website: Mapped[str] = mapped_column(String(512))
    careers_page_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    founded_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
