from incident.factories.incident_client_factory import (
    IncidentClientFactory
)
from incident.models.incident import Incident
from shared.logger import get_logger

logger = get_logger("incident.service")


class IncidentService:

    def __init__(self):
        logger.info("[STEP 1] Initializing IncidentService")
        self.client = IncidentClientFactory.get_client()
        logger.info("[STEP 2] Incident client initialized")

    def create_incident(
        self,
        incident: Incident
    ):
        logger.info(f"[STEP 1] Creating incident | Title : {incident.short_description} | Severity : impact={incident.impact}/urgency={incident.urgency}")
        result = self.client.create_incident(incident)
        logger.info("[STEP 2] Incident creation request sent to provider")
        return result

    def update_incident(
        self,
        incident_number: str,
        payload: dict
    ):
        logger.info(f"[STEP 1] Updating incident : {incident_number}")
        result = self.client.update_incident(incident_number, payload)
        logger.info(f"[STEP 2] Incident updated : {incident_number}")
        return result

    def get_incident(
        self,
        incident_number: str
    ):
        logger.info(f"[STEP 1] Fetching incident : {incident_number}")
        result = self.client.get_incident(incident_number)
        logger.info(f"[STEP 2] Incident retrieved : {incident_number}")
        return result