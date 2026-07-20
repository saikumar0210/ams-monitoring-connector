from incident.models.incident import Incident
from incident.services.incident_service import (
    IncidentService
)

from connector.models import (
    ProcessIncidentRequest
)

from monitoring.models.log_entry import LogEntry
from monitoring.services.monitoring_service import (
    MonitoringService
)
from shared.logger import get_logger

logger = get_logger("connector.service")


class MonitoringConnectorService:

    def __init__(self):

        self.monitoring_service = (
            MonitoringService()
        )

        self.incident_service = (
            IncidentService()
        )

    # =====================================================
    # Logs
    # =====================================================

    def get_all_logs(self):
        logger.info("[STEP 1] Fetching all logs from monitoring service")
        result = self.monitoring_service.get_all_logs()
        logger.info(f"[STEP 2] Retrieved {len(result)} log(s)")
        return result

    def get_error_logs(self):
        logger.info("[STEP 1] Fetching error logs from monitoring service")
        result = self.monitoring_service.get_error_logs()
        logger.info(f"[STEP 2] Retrieved {len(result)} error log(s)")
        return result

    def get_logs_by_service(
        self,
        service_name: str
    ):
        logger.info(f"[STEP 1] Fetching logs for service : {service_name}")
        result = self.monitoring_service.get_logs_by_service(service_name)
        logger.info(f"[STEP 2] Retrieved {len(result)} log(s) for service : {service_name}")
        return result

    def execute_custom_query(
        self,
        query: str
    ):
        logger.info(f"[STEP 1] Executing custom query : {query}")
        result = self.monitoring_service.execute_custom_query(query)
        logger.info(f"[STEP 2] Custom query returned {len(result)} result(s)")
        return result

    # =====================================================
    # Process Incidents
    # =====================================================

    def process_incidents(
        self,
        request: ProcessIncidentRequest
    ):
        logger.info("[STEP 1] Starting incident processing pipeline")

        logger.info("[STEP 2] Fetching error logs from monitoring provider")
        logs = self.monitoring_service.get_error_logs()
        logger.info(f"[STEP 3] Found {len(logs)} error log(s) to process")

        processed_logs = 0
        incidents_created = 0
        failed = 0
        incident_numbers = []

        for log in logs:

            processed_logs += 1
            logger.info(f"[STEP 4.{processed_logs}] Processing log {processed_logs} of {len(logs)}")

            try:

                if isinstance(log, LogEntry):
                    application = log.application
                    service = log.service
                    environment = log.environment
                    severity = log.severity
                    message = log.message
                    monitoring_tool = log.monitoring_tool

                else:
                    application = log.get("application", "Unknown")
                    service = log.get("service", "Unknown")
                    environment = log.get("environment", "Unknown")
                    severity = log.get("severity", "Unknown")
                    message = log.get("message", "No Message")
                    monitoring_tool = log.get("newrelic.source", "New Relic")

                logger.info(f"[STEP 4.{processed_logs}] Building incident | App: {application} | Service: {service} | Severity: {severity}")

                incident = Incident(
                    application=application,
                    service=service,
                    environment=environment,
                    severity=severity,
                    title=message,
                    description=(
                        f"""
Application : {application}

Service : {service}

Environment : {environment}

Severity : {severity}

Message : {message}

Generated automatically from {monitoring_tool}.
"""
                    )
                )

                logger.info(f"[STEP 4.{processed_logs}] Sending incident to incident provider")

                response = self.incident_service.create_incident(incident)

                incident_number = response["result"]["number"]

                logger.info(f"[STEP 4.{processed_logs}] Incident created successfully : {incident_number}")

                incidents_created += 1
                incident_numbers.append(incident_number)

            except Exception as ex:
                failed += 1
                logger.error(f"[STEP 4.{processed_logs}] Failed to create incident : {ex}")

        logger.info(f"[STEP 5] Incident processing complete | Processed: {processed_logs} | Created: {incidents_created} | Failed: {failed}")

        return {
            "processedLogs": processed_logs,
            "incidentsCreated": incidents_created,
            "failed": failed,
            "incidentNumbers": incident_numbers
        }