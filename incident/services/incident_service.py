"""
incident/services/incident_service.py

Service layer for incident operations.
Acts as the intermediary between the connector and the active incident client.
The client is resolved at startup via IncidentClientFactory.
"""
from incident.factories.incident_client_factory import (
    IncidentClientFactory
)
from incident.models.incident import Incident
from shared.logger import get_logger

# Logger scoped to this service
logger = get_logger("incident.service")


class IncidentService:

    def __init__(self):
        logger.info("[STEP 1] Initializing IncidentService")
        # Resolve the correct incident client based on INCIDENT_PROVIDER env var
        self.client = IncidentClientFactory.get_client()
        logger.info("[STEP 2] Incident client initialized")

    # Delegates incident creation to the active provider client
    def create_incident(
        self,
        incident: Incident
    ):
        logger.info(f"[STEP 1] Creating incident | Title : {incident.short_description} | Severity : impact={incident.impact}/urgency={incident.urgency}")
        result = self.client.create_incident(incident)
        logger.info("[STEP 2] Incident creation request sent to provider")
        return result

    # Delegates incident update to the active provider client using the incident number
    def update_incident(
        self,
        incident_number: str,
        payload: dict
    ):
        logger.info(f"[STEP 1] Updating incident : {incident_number}")
        result = self.client.update_incident(incident_number, payload)
        logger.info(f"[STEP 2] Incident updated : {incident_number}")
        return result

    # Delegates incident retrieval to the active provider client using the incident number
    def get_incident(
        self,
        incident_number: str
    ):
        logger.info(f"[STEP 1] Fetching incident : {incident_number}")
        result = self.client.get_incident(incident_number)
        logger.info(f"[STEP 2] Incident retrieved : {incident_number}")
        return result
