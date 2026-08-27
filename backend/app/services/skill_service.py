from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.candidate_profile import CandidateProfile
from app.models.skill import Skill
from app.schemas.skill import SkillCreate, SkillUpdate


def get_candidate_profile(
    db: Session,
    profile_id: int,
) -> CandidateProfile | None:
    return db.scalar(
        select(CandidateProfile).where(
            CandidateProfile.id == profile_id
        )
    )


def create_skill(
    db: Session,
    profile_id: int,
    skill_data: SkillCreate,
) -> Skill | None:

    candidate_profile = get_candidate_profile(
        db=db,
        profile_id=profile_id,
    )

    if candidate_profile is None:
        return None

    skill = Skill(
        candidate_profile_id=profile_id,
        **skill_data.model_dump(),
    )

    db.add(skill)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    db.refresh(skill)

    return skill


def get_skills(
    db: Session,
    profile_id: int,
) -> list[Skill] | None:

    candidate_profile = get_candidate_profile(
        db=db,
        profile_id=profile_id,
    )

    if candidate_profile is None:
        return None

    statement = (
        select(Skill)
        .where(
            Skill.candidate_profile_id == profile_id
        )
        .order_by(
            Skill.category.asc().nullslast(),
            Skill.name.asc(),
        )
    )

    return list(db.scalars(statement).all())


def get_skill(
    db: Session,
    profile_id: int,
    skill_id: int,
) -> Skill | None:

    statement = select(Skill).where(
        Skill.id == skill_id,
        Skill.candidate_profile_id == profile_id,
    )

    return db.scalar(statement)


def update_skill(
    db: Session,
    profile_id: int,
    skill_id: int,
    skill_data: SkillUpdate,
) -> Skill | None:

    skill = get_skill(
        db=db,
        profile_id=profile_id,
        skill_id=skill_id,
    )

    if skill is None:
        return None

    update_data = skill_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(skill, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    db.refresh(skill)

    return skill


def delete_skill(
    db: Session,
    profile_id: int,
    skill_id: int,
) -> bool:

    skill = get_skill(
        db=db,
        profile_id=profile_id,
        skill_id=skill_id,
    )

    if skill is None:
        return False

    db.delete(skill)
    db.commit()

    return True