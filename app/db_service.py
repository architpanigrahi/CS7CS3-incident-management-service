from app.models.db_models import IncidentDBModel
from typing import Optional
import boto3
from datetime import datetime

# Initialize DynamoDB resource
dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-west-2',
    endpoint_url='http://localhost:8000',
    aws_access_key_id='fakeAccessKey',
    aws_secret_access_key='fakeSecretKey'
)

# Table reference
incident_table = dynamodb.Table("Incidents")


def create_incident(data: IncidentDBModel):
    """
    Save a new incident to the database.

    Args:
        data (IncidentDBModel): Incident data to save.

    Returns:
        None
    """
    incident_table.put_item(Item=data.model_dump(by_alias=True))


def get_incident(incident_id: str) -> Optional[IncidentDBModel]:
    """
    Retrieve an incident by its ID.

    Args:
        incident_id (str): The unique identifier of the incident.

    Returns:
        Optional[IncidentDBModel]: The incident record if found, otherwise None.
    """
    response = incident_table.get_item(Key={"incident_id": incident_id})
    item = response.get("Item")
    if not item:
        return None
    return IncidentDBModel.model_validate(item)


def update_incident(incident_id: str, status: str) -> IncidentDBModel:
    """
    Update the status of an incident.

    Args:
        incident_id (str): The unique identifier of the incident.
        status (str): The new status of the incident.

    Returns:
        IncidentDBModel: The updated incident record.
    """
    response = incident_table.update_item(
        Key={"incident_id": incident_id},
        UpdateExpression="SET #status = :status, updated_at = :updated_at",
        ExpressionAttributeNames={"#status": "status"},
        ExpressionAttributeValues={
            ":status": status,
            ":updated_at": datetime.utcnow().isoformat()
        },
        ReturnValues="ALL_NEW"
    )
    return IncidentDBModel.model_validate(response["Attributes"])