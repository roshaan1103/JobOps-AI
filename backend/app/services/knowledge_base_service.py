from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.candidate_profile import CandidateProfile


def get_candidate_knowledge_base(
    db: Session,
    profile_id: int,
) -> CandidateProfile | None:

    statement = (
        select(CandidateProfile)
        .where(
            CandidateProfile.id == profile_id
        )
        .options(
            selectinload(
                CandidateProfile.experiences
            ),
            selectinload(
                CandidateProfile.projects
            ),
            selectinload(
                CandidateProfile.skills
            ),
            selectinload(
                CandidateProfile.certifications
            ),
            selectinload(
                CandidateProfile.education
            ),
        )
    )

    return db.scalar(statement)