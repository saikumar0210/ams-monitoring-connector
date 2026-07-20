from config import Config

from monitoring.clients.new_relic_client import NewRelicClient
from monitoring.clients.datadog_client import DatadogClient
from monitoring.clients.splunk_client import SplunkClient
from monitoring.clients.grafana_client import GrafanaClient
from monitoring.clients.elastic_client import ElasticClient


class MonitoringClientFactory:

    @staticmethod
    def get_client():

        provider = Config.MONITORING_PROVIDER

        if provider == "NEW_RELIC":

            return NewRelicClient()

        if provider == "DATADOG":

            return DatadogClient()

        if provider == "SPLUNK":

            return SplunkClient()

        if provider == "GRAFANA":

            return GrafanaClient()

        if provider == "ELASTIC":

            return ElasticClient()

        raise ValueError(
            f"Unsupported Monitoring Provider : {provider}"
        )