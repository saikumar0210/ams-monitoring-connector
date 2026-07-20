"""
monitoring/factories/monitoring_client_factory.py

Factory that resolves and returns the correct MonitoringClient
based on the MONITORING_PROVIDER environment variable.

Supported providers:
    NEW_RELIC  -> NewRelicClient
    DATADOG    -> DatadogClient
    SPLUNK     -> SplunkClient
    GRAFANA    -> GrafanaClient
    ELASTIC    -> ElasticClient

Raises ValueError for unsupported provider values.
"""
from config import Config

from monitoring.clients.new_relic_client import NewRelicClient
from monitoring.clients.datadog_client import DatadogClient
from monitoring.clients.splunk_client import SplunkClient
from monitoring.clients.grafana_client import GrafanaClient
from monitoring.clients.elastic_client import ElasticClient
from shared.logger import get_logger

# Logger scoped to this factory
logger = get_logger("monitoring.factory")


class MonitoringClientFactory:

    @staticmethod
    def get_client():

        # Read the active monitoring provider from environment config
        provider = Config.MONITORING_PROVIDER
        logger.info(f"[STEP 1] Resolving monitoring client for provider : {provider}")

        # Instantiate and return the matching client implementation
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

        # No matching provider found — fail fast with a clear error message
        logger.error(f"[ERROR] Unsupported monitoring provider : {provider}")
        raise ValueError(
            f"Unsupported Monitoring Provider : {provider}"
        )
