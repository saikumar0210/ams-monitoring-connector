from monitoring.factories.monitoring_client_factory import (
    MonitoringClientFactory
)


class MonitoringService:

    def __init__(self):

        self.client = (
            MonitoringClientFactory.get_client()
        )

    # =====================================================
    # Retrieve All Logs
    # =====================================================

    def get_all_logs(self):

        return self.client.get_all_logs()

    # =====================================================
    # Retrieve Error Logs
    # =====================================================

    def get_error_logs(self):

        return self.client.get_error_logs()

    # =====================================================
    # Retrieve Logs By Service
    # =====================================================

    def get_logs_by_service(
        self,
        service_name: str
    ):

        return self.client.get_logs_by_service(
            service_name
        )

    # =====================================================
    # Execute Custom Query
    # =====================================================

    def execute_custom_query(
        self,
        query: str
    ):

        return self.client.execute_custom_query(
            query
        )