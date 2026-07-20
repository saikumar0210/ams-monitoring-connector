from config import Config

from incident.clients.servicenow_client import ServiceNowClient
from incident.clients.jira_client import JiraClient
from incident.clients.pagerduty_client import PagerDutyClient
from incident.clients.opsgenie_client import OpsGenieClient
from shared.logger import get_logger

logger = get_logger("incident.factory")


class IncidentClientFactory:

    @staticmethod
    def get_client():

        provider = Config.INCIDENT_PROVIDER
        logger.info(f"[STEP 1] Resolving incident client for provider : {provider}")

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

        logger.error(f"[ERROR] Unsupported incident provider : {provider}")
        raise ValueError(
            f"Unsupported Incident Provider : {provider}"
        )