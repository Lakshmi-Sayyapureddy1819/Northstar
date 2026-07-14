"""create company_locations table

Revision ID: 9de5e14af23f
Revises: 010df9e9b35e
Create Date: 2026-07-14 15:07:50.343048

"""

from collections.abc import Sequence

import geoalchemy2
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9de5e14af23f"
down_revision: str | Sequence[str] | None = "010df9e9b35e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # geoalchemy2's Geography(spatial_index=True) auto-creates/drops its GIST
    # index via an event listener on CREATE/DROP TABLE — do not also create it
    # explicitly here, or table creation fails with a duplicate-index error.
    op.create_table(
        "company_locations",
        sa.Column("company_id", sa.Uuid(), nullable=False),
        sa.Column(
            "location",
            geoalchemy2.types.Geography(
                geometry_type="POINT",
                srid=4326,
                dimension=2,
                from_text="ST_GeogFromText",
                name="geography",
                nullable=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.PrimaryKeyConstraint("company_id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("company_locations")
