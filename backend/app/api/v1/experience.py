from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.experience import (
    ExperienceCreate,
    ExperienceResponse,
    ExperienceUpdate,
)
from app.services.experience_service import (
    create_experience,
    delete_experience,
    get_experience,
    get_experiences,
    update_experience,
)


router = APIRouter(
    prefix="/candidate/{profile_id}/experiences",
    tags=["Candidate Experiences"],
)


@router.post(
    "",
    response_model=ExperienceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_candidate_experience(
    profile_id: int,
    experience_data: ExperienceCreate,
    db: Session = Depends(get_db),
):
    experience = create_experience(
        db=db,
        profile_id=profile_id,
        experience_data=experience_data,
    )

    if experience is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate profile not found",
        )

    return experience


@router.get(
    "",
    response_model=list[ExperienceResponse],
)
def list_candidate_experiences(
    profile_id: int,
    db: Session = Depends(get_db),
):
    experiences = get_experiences(
        db=db,
        profile_id=profile_id,
    )

    if experiences is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate profile not found",
        )

    return experiences


@router.get(
    "/{experience_id}",
    response_model=ExperienceResponse,
)
def get_candidate_experience(
    profile_id: int,
    experience_id: int,
    db: Session = Depends(get_db),
):
    experience = get_experience(
        db=db,
        profile_id=profile_id,
        experience_id=experience_id,
    )

    if experience is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience not found",
        )

    return experience


@router.patch(
    "/{experience_id}",
    response_model=ExperienceResponse,
)
def update_candidate_experience(
    profile_id: int,
    experience_id: int,
    experience_data: ExperienceUpdate,
    db: Session = Depends(get_db),
):
    experience = update_experience(
        db=db,
        profile_id=profile_id,
        experience_id=experience_id,
        experience_data=experience_data,
    )

    if experience is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience not found",
        )

    return experience


@router.delete(
    "/{experience_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_candidate_experience(
    profile_id: int,
    experience_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_experience(
        db=db,
        profile_id=profile_id,
        experience_id=experience_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience not found",
        )

    return None