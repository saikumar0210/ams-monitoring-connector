from monitoring.clients.monitoring_client import MonitoringClient


class GrafanaClient(MonitoringClient):

    def get_all_logs(self):

        raise NotImplementedError(
            "Grafana provider is not implemented."
        )

    def get_error_logs(self):

        raise NotImplementedError(
            "Grafana provider is not implemented."
        )

    def get_logs_by_service(
        self,
        service_name: str
    ):

        raise NotImplementedError(
            "Grafana provider is not implemented."
        )

    def execute_custom_query(
        self,
        query: str
    ):

        raise NotImplementedError(
            "Grafana provider is not implemented."
        )