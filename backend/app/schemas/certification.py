from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class CertificationBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )

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

    @model_validator(mode="after")
    def validate_dates(self):
        if self.issue_date and self.expiry_date:
            if self.expiry_date < self.issue_date:
                raise ValueError(
                    "expiry_date cannot be earlier than issue_date"
                )

        return self


class CertificationCreate(CertificationBase):
    pass


class CertificationUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

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

    @model_validator(mode="after")
    def validate_dates(self):
        if self.issue_date and self.expiry_date:
            if self.expiry_date < self.issue_date:
                raise ValueError(
                    "expiry_date cannot be earlier than issue_date"
                )

        return self


class CertificationResponse(CertificationBase):
    id: int
    candidate_profile_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )