from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class CandidateProfileBase(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=255)
    professional_title: str | None = Field(
        default=None,
        max_length=255,
    )
    summary: str | None = None
    phone: str | None = Field(
        default=None,
        max_length=50,
    )
    email: str | None = Field(
        default=None,
        max_length=255,
    )
    linkedin_url: str | None = Field(
        default=None,
        max_length=500,
    )
    github_url: str | None = Field(
        default=None,
        max_length=500,
    )
    portfolio_url: str | None = Field(
        default=None,
        max_length=500,
    )


class CandidateProfileCreate(CandidateProfileBase):
    user_id: int


class CandidateProfileUpdate(BaseModel):
    full_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    professional_title: str | None = Field(
        default=None,
        max_length=255,
    )
    summary: str | None = None
    phone: str | None = Field(
        default=None,
        max_length=50,
    )
    email: str | None = Field(
        default=None,
        max_length=255,
    )
    linkedin_url: str | None = Field(
        default=None,
        max_length=500,
    )
    github_url: str | None = Field(
        default=None,
        max_length=500,
    )
    portfolio_url: str | None = Field(
        default=None,
        max_length=500,
    )


class CandidateProfileResponse(CandidateProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime


class ExperienceCreate(BaseModel):
    company: str = Field(..., min_length=1, max_length=255)
    role: str = Field(..., min_length=1, max_length=255)
    location: str | None = Field(default=None, max_length=255)
    employment_type: str | None = Field(
        default=None,
        max_length=100,
    )
    start_date: date | None = None
    end_date: date | None = None
    is_current: bool = False
    description: str | None = None


class ExperienceResponse(ExperienceCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    candidate_profile_id: int
    created_at: datetime
    updated_at: datetime


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    repository_url: str | None = Field(
        default=None,
        max_length=500,
    )
    live_url: str | None = Field(
        default=None,
        max_length=500,
    )
    start_date: date | None = None
    end_date: date | None = None


class ProjectResponse(ProjectCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    candidate_profile_id: int
    created_at: datetime
    updated_at: datetime


class CertificationCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    issuer: str | None = Field(
        default=None,
        max_length=255,
    )
    credential_id: str | None = Field(
        default=None,
        max_length=255,
    )
    issue_date: date | None = None
    expiry_date: date | None = None
    credential_url: str | None = Field(
        default=None,
        max_length=500,
    )


class CertificationResponse(CertificationCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    candidate_profile_id: int
    created_at: datetime
    updated_at: datetime


class EducationCreate(BaseModel):
    institution: str = Field(..., min_length=1, max_length=255)
    degree: str | None = Field(
        default=None,
        max_length=255,
    )
    field_of_study: str | None = Field(
        default=None,
        max_length=255,
    )
    start_date: date | None = None
    end_date: date | None = None
    description: str | None = None


class EducationResponse(EducationCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    candidate_profile_id: int
    created_at: datetime
    updated_at: datetime


class SkillCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    category: str | None = Field(
        default=None,
        max_length=100,
    )
    proficiency: str | None = Field(
        default=None,
        max_length=100,
    )
    years_experience: float | None = Field(
        default=None,
        ge=0,
    )


class SkillResponse(SkillCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime