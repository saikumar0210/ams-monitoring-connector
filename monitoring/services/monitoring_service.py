from monitoring.factories.monitoring_client_factory import (
    MonitoringClientFactory
)
from shared.logger import get_logger

logger = get_logger("monitoring.service")


class MonitoringService:

    def __init__(self):
        logger.info("[STEP 1] Initializing MonitoringService")
        self.client = MonitoringClientFactory.get_client()
        logger.info("[STEP 2] Monitoring client initialized")

    def get_all_logs(self):
        logger.info("[STEP 1] Querying all logs from monitoring provider")
        result = self.client.get_all_logs()
        logger.info(f"[STEP 2] All logs query complete - {len(result)} record(s) returned")
        return result

    def get_error_logs(self):
        logger.info("[STEP 1] Querying error logs from monitoring provider")
        result = self.client.get_error_logs()
        logger.info(f"[STEP 2] Error logs query complete - {len(result)} record(s) returned")
        return result

    def get_logs_by_service(
        self,
        service_name: str
    ):
        logger.info(f"[STEP 1] Querying logs for service : {service_name}")
        result = self.client.get_logs_by_service(service_name)
        logger.info(f"[STEP 2] Service logs query complete - {len(result)} record(s) returned")
        return result

    def execute_custom_query(
        self,
        query: str
    ):
        logger.info(f"[STEP 1] Executing custom query via monitoring provider")
        result = self.client.execute_custom_query(query)
        logger.info(f"[STEP 2] Custom query complete - {len(result)} record(s) returned")
        return result