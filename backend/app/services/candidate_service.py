from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.candidate_profile import CandidateProfile
from app.models.user import User
from app.schemas.candidate import (
    CandidateProfileCreate,
    CandidateProfileUpdate,
)


def get_candidate_profile(
    db: Session,
    profile_id: int,
) -> CandidateProfile | None:
    statement = select(CandidateProfile).where(
        CandidateProfile.id == profile_id
    )

    return db.scalar(statement)


def get_candidate_profile_by_user(
    db: Session,
    user_id: int,
) -> CandidateProfile | None:
    statement = select(CandidateProfile).where(
        CandidateProfile.user_id == user_id
    )

    return db.scalar(statement)


def create_candidate_profile(
    db: Session,
    profile_data: CandidateProfileCreate,
) -> CandidateProfile:

    user = db.get(User, profile_data.user_id)

    if user is None:
        raise ValueError("User does not exist.")

    existing_profile = get_candidate_profile_by_user(
        db,
        profile_data.user_id,
    )

    if existing_profile is not None:
        raise ValueError(
            "A candidate profile already exists for this user."
        )

    profile = CandidateProfile(
        user_id=profile_data.user_id,
        full_name=profile_data.full_name,
        professional_title=profile_data.professional_title,
        summary=profile_data.summary,
        phone=profile_data.phone,
        email=profile_data.email,
        linkedin_url=profile_data.linkedin_url,
        github_url=profile_data.github_url,
        portfolio_url=profile_data.portfolio_url,
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile


def update_candidate_profile(
    db: Session,
    profile_id: int,
    profile_data: CandidateProfileUpdate,
) -> CandidateProfile | None:

    profile = get_candidate_profile(
        db,
        profile_id,
    )

    if profile is None:
        return None

    update_data = profile_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)

    return profile