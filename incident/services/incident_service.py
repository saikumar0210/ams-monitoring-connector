from incident.factories.incident_client_factory import (
    IncidentClientFactory
)
from incident.models.incident import Incident


class IncidentService:

    def __init__(self):

        self.client = (
            IncidentClientFactory.get_client()
        )

    def create_incident(
        self,
        incident: Incident
    ):

        return self.client.create_incident(
            incident
        )

    def update_incident(
        self,
        incident_number: str,
        payload: dict
    ):

        return self.client.update_incident(
            incident_number,
            payload
        )

    def get_incident(
        self,
        incident_number: str
    ):

        return self.client.get_incident(
            incident_number
        )