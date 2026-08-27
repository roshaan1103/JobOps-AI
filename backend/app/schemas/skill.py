from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SkillBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )

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

    @model_validator(mode="after")
    def normalize_name(self):
        self.name = self.name.strip()
        return self


class SkillCreate(SkillBase):
    pass


class SkillUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

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

    @model_validator(mode="after")
    def normalize_name(self):
        if self.name is not None:
            self.name = self.name.strip()

        return self


class SkillResponse(SkillBase):
    id: int
    candidate_profile_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )