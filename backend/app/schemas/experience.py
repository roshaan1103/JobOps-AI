from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ExperienceBase(BaseModel):
    company: str = Field(..., min_length=1, max_length=255)
    role: str = Field(..., min_length=1, max_length=255)
    location: str | None = Field(default=None, max_length=255)
    employment_type: str | None = Field(default=None, max_length=100)

    start_date: date | None = None
    end_date: date | None = None

    is_current: bool = False

    description: str | None = None

    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValueError("end_date cannot be earlier than start_date")

        if self.is_current and self.end_date is not None:
            raise ValueError(
                "A current experience cannot have an end_date"
            )

        return self


class ExperienceCreate(ExperienceBase):
    pass


class ExperienceUpdate(BaseModel):
    company: str | None = Field(default=None, min_length=1, max_length=255)
    role: str | None = Field(default=None, min_length=1, max_length=255)
    location: str | None = Field(default=None, max_length=255)
    employment_type: str | None = Field(default=None, max_length=100)

    start_date: date | None = None
    end_date: date | None = None

    is_current: bool | None = None

    description: str | None = None

    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValueError("end_date cannot be earlier than start_date")

        if self.is_current is True and self.end_date is not None:
            raise ValueError(
                "A current experience cannot have an end_date"
            )

        return self


class ExperienceResponse(ExperienceBase):
    id: int
    candidate_profile_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)