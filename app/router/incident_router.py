from fastapi import APIRouter, HTTPException

from app.metrics import INCIDENTS_CREATED
from app.models.api_models import CreateIncidentDTO, IncidentDetailDTO, UpdateIncidentDTO
from app.db_service import create_incident, get_incident, update_incident
from app.mappers import map_create_dto_to_db_model, map_db_model_to_detail_dto

router = APIRouter()


@router.post("/incident/report", response_model=IncidentDetailDTO, tags=["Incidents"])
async def create_new_incident(incident: CreateIncidentDTO):
    """
    Create a new incident.

    Args:
        incident (CreateIncidentDTO): The incident details provided by the user.

    Returns:
        IncidentDetailDTO: The created incident.
    """
    db_model = map_create_dto_to_db_model(incident)
    create_incident(db_model)
    INCIDENTS_CREATED.inc()
    return map_db_model_to_detail_dto(db_model)


@router.get("/incident/{incident_id}", response_model=IncidentDetailDTO, tags=["Incidents"])
async def get_incident_details(incident_id: str):
    """
    Fetch details of a specific incident.

    Args:
        incident_id (str): The unique identifier of the incident.

    Returns:
        IncidentDetailDTO: The incident details.
    """
    db_model = get_incident(incident_id)
    if not db_model:
        raise HTTPException(status_code=404, detail="Incident not found")
    return map_db_model_to_detail_dto(db_model)


@router.patch("/incident/{incident_id}", response_model=IncidentDetailDTO, tags=["Incidents"])
async def update_incident_status(incident_id: str, update: UpdateIncidentDTO):
    """
    Update the status of an existing incident.

    Args:
        incident_id (str): The unique identifier of the incident.
        update (UpdateIncidentDTO): The new status to set.

    Returns:
        IncidentDetailDTO: The updated incident details.
    """
    db_model = get_incident(incident_id)
    if not db_model:
        raise HTTPException(status_code=404, detail="Incident not found")

    updated_db_model = update_incident(incident_id, update.status.value)
    return map_db_model_to_detail_dto(updated_db_model)