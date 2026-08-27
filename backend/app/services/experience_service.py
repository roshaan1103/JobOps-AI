from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.candidate_profile import CandidateProfile
from app.models.experience import Experience
from app.schemas.experience import ExperienceCreate, ExperienceUpdate


def get_candidate_profile(
    db: Session,
    profile_id: int,
) -> CandidateProfile | None:
    return db.scalar(
        select(CandidateProfile).where(
            CandidateProfile.id == profile_id
        )
    )


def create_experience(
    db: Session,
    profile_id: int,
    experience_data: ExperienceCreate,
) -> Experience | None:

    candidate_profile = get_candidate_profile(
        db=db,
        profile_id=profile_id,
    )

    if candidate_profile is None:
        return None

    experience = Experience(
        candidate_profile_id=profile_id,
        **experience_data.model_dump(),
    )

    db.add(experience)
    db.commit()
    db.refresh(experience)

    return experience


def get_experiences(
    db: Session,
    profile_id: int,
) -> list[Experience] | None:

    candidate_profile = get_candidate_profile(
        db=db,
        profile_id=profile_id,
    )

    if candidate_profile is None:
        return None

    statement = (
        select(Experience)
        .where(
            Experience.candidate_profile_id == profile_id
        )
        .order_by(
            Experience.start_date.desc().nullslast(),
            Experience.id.desc(),
        )
    )

    return list(db.scalars(statement).all())


def get_experience(
    db: Session,
    profile_id: int,
    experience_id: int,
) -> Experience | None:

    statement = select(Experience).where(
        Experience.id == experience_id,
        Experience.candidate_profile_id == profile_id,
    )

    return db.scalar(statement)


def update_experience(
    db: Session,
    profile_id: int,
    experience_id: int,
    experience_data: ExperienceUpdate,
) -> Experience | None:

    experience = get_experience(
        db=db,
        profile_id=profile_id,
        experience_id=experience_id,
    )

    if experience is None:
        return None

    update_data = experience_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(experience, field, value)

    db.commit()
    db.refresh(experience)

    return experience


def delete_experience(
    db: Session,
    profile_id: int,
    experience_id: int,
) -> bool:

    experience = get_experience(
        db=db,
        profile_id=profile_id,
        experience_id=experience_id,
    )

    if experience is None:
        return False

    db.delete(experience)
    db.commit()

    return True