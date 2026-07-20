from incident.clients.incident_client import IncidentClient
from incident.models.incident import Incident


class JiraClient(IncidentClient):

    def create_incident(
        self,
        incident: Incident
    ):

        raise NotImplementedError(
            "Jira integration is not implemented."
        )

    def get_incident(
        self,
        incident_number: str
    ):

        raise NotImplementedError(
            "Jira integration is not implemented."
        )

    def update_incident(
        self,
        incident_number: str,
        payload: dict
    ):

        raise NotImplementedError(
            "Jira integration is not implemented."
        )