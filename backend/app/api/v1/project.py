from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.project import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)
from app.services.project_service import (
    create_project,
    delete_project,
    get_project,
    get_projects,
    update_project,
)


router = APIRouter(
    prefix="/candidate/{profile_id}/projects",
    tags=["Candidate Projects"],
)


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_candidate_project(
    profile_id: int,
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
):
    project = create_project(
        db=db,
        profile_id=profile_id,
        project_data=project_data,
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate profile not found",
        )

    return project


@router.get(
    "",
    response_model=list[ProjectResponse],
)
def list_candidate_projects(
    profile_id: int,
    db: Session = Depends(get_db),
):
    projects = get_projects(
        db=db,
        profile_id=profile_id,
    )

    if projects is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate profile not found",
        )

    return projects


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
)
def get_candidate_project(
    profile_id: int,
    project_id: int,
    db: Session = Depends(get_db),
):
    project = get_project(
        db=db,
        profile_id=profile_id,
        project_id=project_id,
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return project


@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
)
def update_candidate_project(
    profile_id: int,
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
):
    project = update_project(
        db=db,
        profile_id=profile_id,
        project_id=project_id,
        project_data=project_data,
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return project


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_candidate_project(
    profile_id: int,
    project_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_project(
        db=db,
        profile_id=profile_id,
        project_id=project_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return None