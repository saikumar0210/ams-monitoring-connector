from config import Config

from incident.clients.servicenow_client import ServiceNowClient
from incident.clients.jira_client import JiraClient
from incident.clients.pagerduty_client import PagerDutyClient
from incident.clients.opsgenie_client import OpsGenieClient


class IncidentClientFactory:

    @staticmethod
    def get_client():

        provider = Config.INCIDENT_PROVIDER

        if provider == "SERVICENOW":
            return ServiceNowClient()

        if provider == "JIRA":
            return JiraClient()

        if provider == "PAGERDUTY":
            return PagerDutyClient()

        if provider == "OPSGENIE":
            return OpsGenieClient()

        raise ValueError(
            f"Unsupported Incident Provider : {provider}"
        )