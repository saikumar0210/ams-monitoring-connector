"""
incident/factories/incident_client_factory.py

Factory that resolves and returns the correct IncidentClient
based on the INCIDENT_PROVIDER environment variable.

Supported providers:
    SERVICENOW  -> ServiceNowClient
    JIRA        -> JiraClient
    PAGERDUTY   -> PagerDutyClient
    OPSGENIE    -> OpsGenieClient

Raises ValueError for unsupported provider values.
"""
from config import Config

from incident.clients.servicenow_client import ServiceNowClient
from incident.clients.jira_client import JiraClient
from incident.clients.pagerduty_client import PagerDutyClient
from incident.clients.opsgenie_client import OpsGenieClient
from shared.logger import get_logger

# Logger scoped to this factory
logger = get_logger("incident.factory")


class IncidentClientFactory:

    @staticmethod
    def get_client():

        # Read the active incident provider from environment config
        provider = Config.INCIDENT_PROVIDER
        logger.info(f"[STEP 1] Resolving incident client for provider : {provider}")

        # Instantiate and return the matching client implementation
        if provider == "SERVICENOW":
            logger.info("[STEP 2] Selected client : ServiceNowClient")
            return ServiceNowClient()

        if provider == "JIRA":
            logger.info("[STEP 2] Selected client : JiraClient")
            return JiraClient()

        if provider == "PAGERDUTY":
            logger.info("[STEP 2] Selected client : PagerDutyClient")
            return PagerDutyClient()

        if provider == "OPSGENIE":
            logger.info("[STEP 2] Selected client : OpsGenieClient")
            return OpsGenieClient()

        # No matching provider found — fail fast with a clear error message
        logger.error(f"[ERROR] Unsupported incident provider : {provider}")
        raise ValueError(
            f"Unsupported Incident Provider : {provider}"
        )
