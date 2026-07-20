from incident.clients.incident_client import IncidentClient
from incident.models.incident import Incident


class PagerDutyClient(IncidentClient):

    def create_incident(
        self,
        incident: Incident
    ):

        raise NotImplementedError(
            "PagerDuty integration is not implemented."
        )

    def get_incident(
        self,
        incident_number: str
    ):

        raise NotImplementedError(
            "PagerDuty integration is not implemented."
        )

    def update_incident(
        self,
        incident_number: str,
        payload: dict
    ):

        raise NotImplementedError(
            "PagerDuty integration is not implemented."
        )