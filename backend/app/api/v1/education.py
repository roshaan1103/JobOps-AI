from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.education import (
    EducationCreate,
    EducationResponse,
    EducationUpdate,
)
from app.services.education_service import (
    create_education,
    delete_education,
    get_education,
    get_educations,
    update_education,
)


router = APIRouter(
    prefix="/candidate/{profile_id}/education",
    tags=["Candidate Education"],
)


@router.post(
    "",
    response_model=EducationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_candidate_education(
    profile_id: int,
    education_data: EducationCreate,
    db: Session = Depends(get_db),
):
    education = create_education(
        db=db,
        profile_id=profile_id,
        education_data=education_data,
    )

    if education is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate profile not found",
        )

    return education


@router.get(
    "",
    response_model=list[EducationResponse],
)
def list_candidate_education(
    profile_id: int,
    db: Session = Depends(get_db),
):
    education_records = get_educations(
        db=db,
        profile_id=profile_id,
    )

    if education_records is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate profile not found",
        )

    return education_records


@router.get(
    "/{education_id}",
    response_model=EducationResponse,
)
def get_candidate_education(
    profile_id: int,
    education_id: int,
    db: Session = Depends(get_db),
):
    education = get_education(
        db=db,
        profile_id=profile_id,
        education_id=education_id,
    )

    if education is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Education record not found",
        )

    return education


@router.patch(
    "/{education_id}",
    response_model=EducationResponse,
)
def update_candidate_education(
    profile_id: int,
    education_id: int,
    education_data: EducationUpdate,
    db: Session = Depends(get_db),
):
    education = update_education(
        db=db,
        profile_id=profile_id,
        education_id=education_id,
        education_data=education_data,
    )

    if education is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Education record not found",
        )

    return education


@router.delete(
    "/{education_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_candidate_education(
    profile_id: int,
    education_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_education(
        db=db,
        profile_id=profile_id,
        education_id=education_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Education record not found",
        )

    return None