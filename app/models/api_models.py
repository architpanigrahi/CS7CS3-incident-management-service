from enum import Enum
from pydantic import BaseModel, Field, field_validator


class SeverityEnum(str, Enum):
    """
    Enum representing the severity levels of an incident.
    """
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class StatusEnum(str, Enum):
    """
    Enum representing the various statuses an incident can have during its lifecycle.
    """
    REPORTED = "Reported"
    IN_PROGRESS = "Verification in Progress"
    DUPLICATE = "Duplicate"
    VERIFIED = "Verified"
    RESOLVED = "Resolved"


class IncidentTypeEnum(str, Enum):
    """
    Enum for categorizing incidents into specific types.
    """
    FIRE = "Fire"
    FLOOD = "Flood"
    EARTHQUAKE = "Earthquake"
    CRIMINAL = "Criminal"
    OTHER = "Other"


class IncidentLocationDTO(BaseModel):
    """
    Represents the geographic location of an incident.
    """
    latitude: float = Field(
        ...,
        title="Latitude",
        description="Latitude of the incident location (in degrees).",
        examples=[53.3498]
    )
    longitude: float = Field(
        ...,
        title="Longitude",
        description="Longitude of the incident location (in degrees).",
        examples=[-6.2603]
    )


class CreateIncidentDTO(BaseModel):
    """
    Represents the data required to create a new incident.
    """
    location: IncidentLocationDTO = Field(
        ...,
        title="Incident Location",
        description="The geographic location where the incident occurred."
    )
    type: IncidentTypeEnum = Field(
        ...,
        title="Incident Type",
        description="The category of the incident (e.g., Fire, Flood).",
        examples=["Fire"]
    )
    severity: SeverityEnum = Field(
        ...,
        title="Severity Level",
        description="The severity level of the incident.",
        examples=["High"]
    )
    user_id: str = Field(
        ...,
        title="User ID",
        description="The unique identifier of the user reporting the incident.",
        examples=["user123"]
    )

    @field_validator("user_id")
    def validate_user_id(cls, value):
        """
        Validates that the `user_id` field is not empty.
        """
        if len(value.strip()) == 0:
            raise ValueError("User ID cannot be empty.")
        return value


class IncidentDetailDTO(BaseModel):
    """
    Represents detailed information about an incident, including its status.
    """
    incident_id: str = Field(
        ...,
        title="Incident ID",
        description="The unique identifier for the incident.",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    location: IncidentLocationDTO = Field(
        ...,
        title="Incident Location",
        description="The geographic location where the incident occurred."
    )
    type: IncidentTypeEnum = Field(
        ...,
        title="Incident Type",
        description="The category of the incident (e.g., Fire, Flood).",
        examples=["Fire"]
    )
    severity: SeverityEnum = Field(
        ...,
        title="Severity Level",
        description="The severity level of the incident.",
        examples=["High"]
    )
    user_id: str = Field(
        ...,
        title="User ID",
        description="The unique identifier of the user who reported the incident.",
        examples=["user123"]
    )
    status: StatusEnum = Field(
        ...,
        title="Incident Status",
        description="The current status of the incident.",
        examples=["Reported"]
    )


class UpdateIncidentDTO(BaseModel):
    """
    Represents the data required to update the status of an existing incident.
    """
    status: StatusEnum = Field(
        ...,
        title="Incident Status",
        description="The new status of the incident.",
        examples=["Resolved"]
    )