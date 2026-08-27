from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.candidate_profile import CandidateProfile
from app.models.certification import Certification
from app.schemas.certification import (
    CertificationCreate,
    CertificationUpdate,
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


def create_certification(
    db: Session,
    profile_id: int,
    certification_data: CertificationCreate,
) -> Certification | None:

    candidate_profile = get_candidate_profile(
        db=db,
        profile_id=profile_id,
    )

    if candidate_profile is None:
        return None

    certification = Certification(
        candidate_profile_id=profile_id,
        **certification_data.model_dump(),
    )

    db.add(certification)
    db.commit()
    db.refresh(certification)

    return certification


def get_certifications(
    db: Session,
    profile_id: int,
) -> list[Certification] | None:

    candidate_profile = get_candidate_profile(
        db=db,
        profile_id=profile_id,
    )

    if candidate_profile is None:
        return None

    statement = (
        select(Certification)
        .where(
            Certification.candidate_profile_id == profile_id
        )
        .order_by(
            Certification.issue_date.desc().nullslast(),
            Certification.id.desc(),
        )
    )

    return list(db.scalars(statement).all())


def get_certification(
    db: Session,
    profile_id: int,
    certification_id: int,
) -> Certification | None:

    statement = select(Certification).where(
        Certification.id == certification_id,
        Certification.candidate_profile_id == profile_id,
    )

    return db.scalar(statement)


def update_certification(
    db: Session,
    profile_id: int,
    certification_id: int,
    certification_data: CertificationUpdate,
) -> Certification | None:

    certification = get_certification(
        db=db,
        profile_id=profile_id,
        certification_id=certification_id,
    )

    if certification is None:
        return None

    update_data = certification_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(certification, field, value)

    db.commit()
    db.refresh(certification)

    return certification


def delete_certification(
    db: Session,
    profile_id: int,
    certification_id: int,
) -> bool:

    certification = get_certification(
        db=db,
        profile_id=profile_id,
        certification_id=certification_id,
    )

    if certification is None:
        return False

    db.delete(certification)
    db.commit()

    return True