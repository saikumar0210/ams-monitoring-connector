"""
incident/clients/opsgenie_client.py

Incident client stub for OpsGenie.
Not yet implemented — raises NotImplementedError for all operations.
"""
from incident.clients.incident_client import IncidentClient
from incident.models.incident import Incident


class OpsGenieClient(IncidentClient):

    def create_incident(
        self,
        incident: Incident
    ):

        raise NotImplementedError(
            "OpsGenie integration is not implemented."
        )

    def get_incident(
        self,
        incident_number: str
    ):

        raise NotImplementedError(
            "OpsGenie integration is not implemented."
        )

    def update_incident(
        self,
        incident_number: str,
        payload: dict
    ):

        raise NotImplementedError(
            "OpsGenie integration is not implemented."
        )
