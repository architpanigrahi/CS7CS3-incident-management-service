import uuid
from decimal import Decimal, ROUND_HALF_UP
from app.models.api_models import *
from app.models.db_models import IncidentDBModel
from datetime import datetime


def map_create_dto_to_db_model(dto: CreateIncidentDTO) -> IncidentDBModel:
    """
    Maps a CreateIncidentDTO to IncidentDBModel for database storage.

    Args:
        dto (CreateIncidentDTO): The input DTO from the API layer.

    Returns:
        IncidentDBModel: The model ready for database insertion.
    """
    def to_exact_decimal(value: float, precision: str = ".0001") -> Decimal:
        """
        Converts a float to an exact Decimal with the specified precision.

        Args:
            value (float): The float value to convert.
            precision (str): The precision format (default is 4 decimal places).

        Returns:
            Decimal: The quantized Decimal value.
        """
        return Decimal(value).quantize(Decimal(precision), rounding=ROUND_HALF_UP)

    return IncidentDBModel(
        incident_id=str(uuid.uuid4()),  # Generate unique ID
        location={
            "latitude": to_exact_decimal(dto.location.latitude),  # Ensure exact precision
            "longitude": to_exact_decimal(dto.location.longitude)  # Ensure exact precision
        },
        type=dto.type.value,
        severity=dto.severity.value,
        user_id=dto.user_id,
        status="Reported",
        created_at=datetime.utcnow().isoformat(),
        updated_at=None
    )


def map_db_model_to_detail_dto(db_model: IncidentDBModel) -> IncidentDetailDTO:
    """
    Maps an IncidentDBModel to IncidentDetailDTO for API response.

    Args:
        db_model (IncidentDBModel): The database model retrieved from storage.

    Returns:
        IncidentDetailDTO: The DTO ready to be returned in the API response.
    """
    return IncidentDetailDTO(
        incident_id=db_model.incident_id,
        location=IncidentLocationDTO(
            latitude=float(db_model.location["latitude"]),  # Convert Decimal back to float
            longitude=float(db_model.location["longitude"])  # Convert Decimal back to float
        ),
        type=IncidentTypeEnum(db_model.type),
        severity=SeverityEnum(db_model.severity),
        user_id=db_model.user_id,
        status=StatusEnum(db_model.status)
    )


def update_db_model_with_status(db_model: IncidentDBModel, status: str) -> IncidentDBModel:
    """
    Updates the status and updated_at timestamp in an IncidentDBModel.

    Args:
        db_model (IncidentDBModel): The existing database model.
        status (str): The new status to set.

    Returns:
        IncidentDBModel: The updated database model.
    """
    db_model.status = status
    db_model.updated_at = datetime.utcnow().isoformat()
    return db_model