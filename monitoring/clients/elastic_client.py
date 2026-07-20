from monitoring.clients.monitoring_client import MonitoringClient


class ElasticClient(MonitoringClient):

    def get_all_logs(self):

        raise NotImplementedError(
            "Elastic provider is not implemented."
        )

    def get_error_logs(self):

        raise NotImplementedError(
            "Elastic provider is not implemented."
        )

    def get_logs_by_service(
        self,
        service_name: str
    ):

        raise NotImplementedError(
            "Elastic provider is not implemented."
        )

    def execute_custom_query(
        self,
        query: str
    ):

        raise NotImplementedError(
            "Elastic provider is not implemented."
        )