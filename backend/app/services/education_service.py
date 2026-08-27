from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.candidate_profile import CandidateProfile
from app.models.education import Education
from app.schemas.education import (
    EducationCreate,
    EducationUpdate,
)


def get_candidate_profile(
    db: Session,
    profile_id: int,
) -> CandidateProfile | None:
    return db.scalar(
        select(CandidateProfile).where(
            CandidateProfile.id == profile_id
        )
    )


def create_education(
    db: Session,
    profile_id: int,
    education_data: EducationCreate,
) -> Education | None:

    candidate_profile = get_candidate_profile(
        db=db,
        profile_id=profile_id,
    )

    if candidate_profile is None:
        return None

    education = Education(
        candidate_profile_id=profile_id,
        **education_data.model_dump(),
    )

    db.add(education)
    db.commit()
    db.refresh(education)

    return education


def get_educations(
    db: Session,
    profile_id: int,
) -> list[Education] | None:

    candidate_profile = get_candidate_profile(
        db=db,
        profile_id=profile_id,
    )

    if candidate_profile is None:
        return None

    statement = (
        select(Education)
        .where(
            Education.candidate_profile_id == profile_id
        )
        .order_by(
            Education.start_date.desc().nullslast(),
            Education.id.desc(),
        )
    )

    return list(db.scalars(statement).all())


def get_education(
    db: Session,
    profile_id: int,
    education_id: int,
) -> Education | None:

    statement = select(Education).where(
        Education.id == education_id,
        Education.candidate_profile_id == profile_id,
    )

    return db.scalar(statement)


def update_education(
    db: Session,
    profile_id: int,
    education_id: int,
    education_data: EducationUpdate,
) -> Education | None:

    education = get_education(
        db=db,
        profile_id=profile_id,
        education_id=education_id,
    )

    if education is None:
        return None

    update_data = education_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(education, field, value)

    db.commit()
    db.refresh(education)

    return education


def delete_education(
    db: Session,
    profile_id: int,
    education_id: int,
) -> bool:

    education = get_education(
        db=db,
        profile_id=profile_id,
        education_id=education_id,
    )

    if education is None:
        return False

    db.delete(education)
    db.commit()

    return True