"""associate skills with candidate profiles

Revision ID: 5de1008d13af
Revises: bed89c6f8a3d
Create Date: 2026-08-27 12:20:16.458748

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5de1008d13af"
down_revision: Union[str, Sequence[str], None] = "bed89c6f8a3d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "skills",
        sa.Column(
            "candidate_profile_id",
            sa.Integer(),
            nullable=False,
        ),
    )

    op.drop_index(
        op.f("ix_skills_name"),
        table_name="skills",
    )

    op.create_index(
        op.f("ix_skills_name"),
        "skills",
        ["name"],
        unique=False,
    )

    op.create_index(
        op.f("ix_skills_candidate_profile_id"),
        "skills",
        ["candidate_profile_id"],
        unique=False,
    )

    op.create_unique_constraint(
        "uq_candidate_skill_name",
        "skills",
        ["candidate_profile_id", "name"],
    )

    op.create_foreign_key(
        "fk_skills_candidate_profile",
        "skills",
        "candidate_profiles",
        ["candidate_profile_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        "fk_skills_candidate_profile",
        "skills",
        type_="foreignkey",
    )

    op.drop_constraint(
        "uq_candidate_skill_name",
        "skills",
        type_="unique",
    )

    op.drop_index(
        op.f("ix_skills_candidate_profile_id"),
        table_name="skills",
    )

    op.drop_index(
        op.f("ix_skills_name"),
        table_name="skills",
    )

    op.create_index(
        op.f("ix_skills_name"),
        "skills",
        ["name"],
        unique=True,
    )

    op.drop_column(
        "skills",
        "candidate_profile_id",
    )