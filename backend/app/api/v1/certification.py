from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.certification import (
    CertificationCreate,
    CertificationResponse,
    CertificationUpdate,
)
from app.services.certification_service import (
    create_certification,
    delete_certification,
    get_certification,
    get_certifications,
    update_certification,
)


router = APIRouter(
    prefix="/candidate/{profile_id}/certifications",
    tags=["Candidate Certifications"],
)


@router.post(
    "",
    response_model=CertificationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_candidate_certification(
    profile_id: int,
    certification_data: CertificationCreate,
    db: Session = Depends(get_db),
):
    certification = create_certification(
        db=db,
        profile_id=profile_id,
        certification_data=certification_data,
    )

    if certification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate profile not found",
        )

    return certification


@router.get(
    "",
    response_model=list[CertificationResponse],
)
def list_candidate_certifications(
    profile_id: int,
    db: Session = Depends(get_db),
):
    certifications = get_certifications(
        db=db,
        profile_id=profile_id,
    )

    if certifications is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate profile not found",
        )

    return certifications


@router.get(
    "/{certification_id}",
    response_model=CertificationResponse,
)
def get_candidate_certification(
    profile_id: int,
    certification_id: int,
    db: Session = Depends(get_db),
):
    certification = get_certification(
        db=db,
        profile_id=profile_id,
        certification_id=certification_id,
    )

    if certification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certification not found",
        )

    return certification


@router.patch(
    "/{certification_id}",
    response_model=CertificationResponse,
)
def update_candidate_certification(
    profile_id: int,
    certification_id: int,
    certification_data: CertificationUpdate,
    db: Session = Depends(get_db),
):
    certification = update_certification(
        db=db,
        profile_id=profile_id,
        certification_id=certification_id,
        certification_data=certification_data,
    )

    if certification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certification not found",
        )

    return certification


@router.delete(
    "/{certification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_candidate_certification(
    profile_id: int,
    certification_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_certification(
        db=db,
        profile_id=profile_id,
        certification_id=certification_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certification not found",
        )

    return None