from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.candidate_profile import CandidateProfile
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


def get_candidate_profile(
    db: Session,
    profile_id: int,
) -> CandidateProfile | None:
    return db.scalar(
        select(CandidateProfile).where(
            CandidateProfile.id == profile_id
        )
    )


def create_project(
    db: Session,
    profile_id: int,
    project_data: ProjectCreate,
) -> Project | None:

    candidate_profile = get_candidate_profile(
        db=db,
        profile_id=profile_id,
    )

    if candidate_profile is None:
        return None

    project = Project(
        candidate_profile_id=profile_id,
        **project_data.model_dump(),
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


def get_projects(
    db: Session,
    profile_id: int,
) -> list[Project] | None:

    candidate_profile = get_candidate_profile(
        db=db,
        profile_id=profile_id,
    )

    if candidate_profile is None:
        return None

    statement = (
        select(Project)
        .where(
            Project.candidate_profile_id == profile_id
        )
        .order_by(
            Project.start_date.desc().nullslast(),
            Project.id.desc(),
        )
    )

    return list(db.scalars(statement).all())


def get_project(
    db: Session,
    profile_id: int,
    project_id: int,
) -> Project | None:

    statement = select(Project).where(
        Project.id == project_id,
        Project.candidate_profile_id == profile_id,
    )

    return db.scalar(statement)


def update_project(
    db: Session,
    profile_id: int,
    project_id: int,
    project_data: ProjectUpdate,
) -> Project | None:

    project = get_project(
        db=db,
        profile_id=profile_id,
        project_id=project_id,
    )

    if project is None:
        return None

    update_data = project_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)

    return project


def delete_project(
    db: Session,
    profile_id: int,
    project_id: int,
) -> bool:

    project = get_project(
        db=db,
        profile_id=profile_id,
        project_id=project_id,
    )

    if project is None:
        return False

    db.delete(project)
    db.commit()

    return True