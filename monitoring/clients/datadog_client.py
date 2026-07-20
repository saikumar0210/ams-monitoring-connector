"""
monitoring/clients/datadog_client.py

Monitoring client stub for Datadog.
Not yet implemented — raises NotImplementedError for all operations.
"""
from monitoring.clients.monitoring_client import MonitoringClient


class DatadogClient(MonitoringClient):

    def get_all_logs(self):

        raise NotImplementedError(
            "Datadog provider is not implemented."
        )

    def get_error_logs(self):

        raise NotImplementedError(
            "Datadog provider is not implemented."
        )

    def get_logs_by_service(
        self,
        service_name: str
    ):

        raise NotImplementedError(
            "Datadog provider is not implemented."
        )

    def execute_custom_query(
        self,
        query: str
    ):

        raise NotImplementedError(
            "Datadog provider is not implemented."
        )