from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.candidate import (
    CandidateProfileCreate,
    CandidateProfileResponse,
    CandidateProfileUpdate,
)
from app.services.candidate_service import (
    create_candidate_profile,
    get_candidate_profile,
    get_candidate_profile_by_user,
    update_candidate_profile,
)


router = APIRouter(
    prefix="/candidate",
    tags=["Candidate"],
)


@router.get(
    "/{profile_id}",
    response_model=CandidateProfileResponse,
)
def get_candidate(
    profile_id: int,
    db: Session = Depends(get_db),
):
    profile = get_candidate_profile(
        db,
        profile_id,
    )

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate profile not found.",
        )

    return profile


@router.get(
    "/user/{user_id}",
    response_model=CandidateProfileResponse,
)
def get_candidate_by_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    profile = get_candidate_profile_by_user(
        db,
        user_id,
    )

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate profile not found.",
        )

    return profile


@router.post(
    "/",
    response_model=CandidateProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_candidate(
    profile_data: CandidateProfileCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_candidate_profile(
            db,
            profile_data,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.patch(
    "/{profile_id}",
    response_model=CandidateProfileResponse,
)
def update_candidate(
    profile_id: int,
    profile_data: CandidateProfileUpdate,
    db: Session = Depends(get_db),
):
    profile = update_candidate_profile(
        db,
        profile_id,
        profile_data,
    )

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate profile not found.",
        )

    return profile