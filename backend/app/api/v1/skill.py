from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.skill import (
    SkillCreate,
    SkillResponse,
    SkillUpdate,
)
from app.services.skill_service import (
    create_skill,
    delete_skill,
    get_skill,
    get_skills,
    update_skill,
)


router = APIRouter(
    prefix="/candidate/{profile_id}/skills",
    tags=["Candidate Skills"],
)


@router.post(
    "",
    response_model=SkillResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_candidate_skill(
    profile_id: int,
    skill_data: SkillCreate,
    db: Session = Depends(get_db),
):
    try:
        skill = create_skill(
            db=db,
            profile_id=profile_id,
            skill_data=skill_data,
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This skill already exists for this candidate profile",
        )

    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate profile not found",
        )

    return skill


@router.get(
    "",
    response_model=list[SkillResponse],
)
def list_candidate_skills(
    profile_id: int,
    db: Session = Depends(get_db),
):
    skills = get_skills(
        db=db,
        profile_id=profile_id,
    )

    if skills is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate profile not found",
        )

    return skills


@router.get(
    "/{skill_id}",
    response_model=SkillResponse,
)
def get_candidate_skill(
    profile_id: int,
    skill_id: int,
    db: Session = Depends(get_db),
):
    skill = get_skill(
        db=db,
        profile_id=profile_id,
        skill_id=skill_id,
    )

    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found",
        )

    return skill


@router.patch(
    "/{skill_id}",
    response_model=SkillResponse,
)
def update_candidate_skill(
    profile_id: int,
    skill_id: int,
    skill_data: SkillUpdate,
    db: Session = Depends(get_db),
):
    try:
        skill = update_skill(
            db=db,
            profile_id=profile_id,
            skill_id=skill_id,
            skill_data=skill_data,
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This skill already exists for this candidate profile",
        )

    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found",
        )

    return skill


@router.delete(
    "/{skill_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_candidate_skill(
    profile_id: int,
    skill_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_skill(
        db=db,
        profile_id=profile_id,
        skill_id=skill_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found",
        )

    return None