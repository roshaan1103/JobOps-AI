from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ProjectBase(BaseModel):
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

    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValueError(
                    "end_date cannot be earlier than start_date"
                )

        return self


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

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

    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValueError(
                    "end_date cannot be earlier than start_date"
                )

        return self


class ProjectResponse(ProjectBase):
    id: int
    candidate_profile_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)