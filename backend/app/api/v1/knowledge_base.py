from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.knowledge_base import CandidateKnowledgeBase
from app.services.knowledge_base_service import (
    get_candidate_knowledge_base,
)


router = APIRouter(
    prefix="/candidate/{profile_id}/knowledge-base",
    tags=["Candidate Knowledge Base"],
)


@router.get(
    "",
    response_model=CandidateKnowledgeBase,
)
def get_candidate_knowledge_base_endpoint(
    profile_id: int,
    db: Session = Depends(get_db),
):
    candidate_profile = get_candidate_knowledge_base(
        db=db,
        profile_id=profile_id,
    )

    if candidate_profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate profile not found",
        )

    return candidate_profile