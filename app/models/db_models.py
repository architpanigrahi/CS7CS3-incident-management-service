from decimal import Decimal

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class IncidentDBModel(BaseModel):
    """
    Represents the DynamoDB schema for storing incident data.
    """
    incident_id: str = Field(..., alias="incident_id", description="Primary key for the incident (Incident ID).")
    location: dict = Field(
        ...,
        description="Geographic location of the incident.",
        examples=[{"latitude": 53.3498, "longitude": -6.2603}]
    )
    type: str = Field(
        ...,
        description="Type of the incident (e.g., Fire, Flood).",
        examples=["Fire"]
    )
    severity: str = Field(
        ...,
        description="Severity level of the incident.",
        examples=["High"]
    )
    user_id: str = Field(
        ...,
        description="Unique identifier of the user who reported the incident.",
        examples=["user123"]
    )
    status: str = Field(
        ...,
        description="Current status of the incident.",
        examples=["Reported"]
    )
    created_at: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        description="Timestamp when the incident was created."
    )
    updated_at: Optional[str] = Field(
        default=None,
        description="Timestamp when the incident was last updated."
    )

    class Config:
        """
        Pydantic model configuration for aliasing.
        """
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if isinstance(v, datetime) else v
        }

