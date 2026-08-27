from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class KnowledgeBaseExperience(BaseModel):
    id: int
    company: str
    role: str
    location: str | None
    employment_type: str | None
    start_date: date | None
    end_date: date | None
    is_current: bool
    description: str | None

    model_config = ConfigDict(
        from_attributes=True,
    )


class KnowledgeBaseProject(BaseModel):
    id: int
    name: str
    description: str | None
    repository_url: str | None
    live_url: str | None
    start_date: date | None
    end_date: date | None

    model_config = ConfigDict(
        from_attributes=True,
    )


class KnowledgeBaseSkill(BaseModel):
    id: int
    name: str
    category: str | None
    proficiency: str | None
    years_experience: float | None

    model_config = ConfigDict(
        from_attributes=True,
    )


class KnowledgeBaseCertification(BaseModel):
    id: int
    name: str
    issuer: str | None
    credential_id: str | None
    issue_date: date | None
    expiry_date: date | None
    credential_url: str | None

    model_config = ConfigDict(
        from_attributes=True,
    )


class KnowledgeBaseEducation(BaseModel):
    id: int
    institution: str
    degree: str | None
    field_of_study: str | None
    start_date: date | None
    end_date: date | None
    description: str | None

    model_config = ConfigDict(
        from_attributes=True,
    )


class CandidateKnowledgeBase(BaseModel):
    id: int
    user_id: int
    full_name: str
    professional_title: str | None
    summary: str | None
    phone: str | None
    email: str | None
    linkedin_url: str | None
    github_url: str | None
    portfolio_url: str | None

    created_at: datetime
    updated_at: datetime

    experiences: list[KnowledgeBaseExperience]
    projects: list[KnowledgeBaseProject]
    skills: list[KnowledgeBaseSkill]
    certifications: list[KnowledgeBaseCertification]
    education: list[KnowledgeBaseEducation]

    model_config = ConfigDict(
        from_attributes=True,
    )