from config import Config

from monitoring.clients.new_relic_client import NewRelicClient
from monitoring.clients.datadog_client import DatadogClient
from monitoring.clients.splunk_client import SplunkClient
from monitoring.clients.grafana_client import GrafanaClient
from monitoring.clients.elastic_client import ElasticClient
from shared.logger import get_logger

logger = get_logger("monitoring.factory")


class MonitoringClientFactory:

    @staticmethod
    def get_client():

        provider = Config.MONITORING_PROVIDER
        logger.info(f"[STEP 1] Resolving monitoring client for provider : {provider}")

        if provider == "NEW_RELIC":
            logger.info("[STEP 2] Selected client : NewRelicClient")
            return NewRelicClient()

        if provider == "DATADOG":
            logger.info("[STEP 2] Selected client : DatadogClient")
            return DatadogClient()

        if provider == "SPLUNK":
            logger.info("[STEP 2] Selected client : SplunkClient")
            return SplunkClient()

        if provider == "GRAFANA":
            logger.info("[STEP 2] Selected client : GrafanaClient")
            return GrafanaClient()

        if provider == "ELASTIC":
            logger.info("[STEP 2] Selected client : ElasticClient")
            return ElasticClient()

        logger.error(f"[ERROR] Unsupported monitoring provider : {provider}")
        raise ValueError(
            f"Unsupported Monitoring Provider : {provider}"
        )