"""
connector/services/monitoring_connector_service.py

Orchestration layer that bridges the monitoring and incident pipelines.

Responsibilities:
    - Delegates log retrieval to MonitoringService
    - Orchestrates the process-incidents pipeline:
        1. Fetches error logs from the monitoring provider
        2. Maps each log to an Incident object
        3. Submits each incident to the incident provider via IncidentService
        4. Returns a summary of processed, created, and failed incidents
"""
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
import requests

from config import Config

# Logger scoped to this service for pipeline tracing
logger = get_logger("connector.service")


class MonitoringConnectorService:

    def __init__(self):
        # Initialize both services — each resolves their provider client via factory
        self.monitoring_service = (
            MonitoringService()
        )

        self.incident_service = (
            IncidentService()
        )

    # =====================================================
    # Logs
    # =====================================================

    # Delegates to MonitoringService which calls the active monitoring provider client
    def get_all_logs(self):
        logger.info("[STEP 1] Fetching all logs from monitoring service")
        result = self.monitoring_service.get_all_logs()
        logger.info(f"[STEP 2] Retrieved {len(result)} log(s)")
        return result

    # Delegates to MonitoringService — only ERROR and CRITICAL logs are returned
    def get_error_logs(self):
        logger.info("[STEP 1] Fetching error logs from monitoring service")
        result = self.monitoring_service.get_error_logs()
        logger.info(f"[STEP 2] Retrieved {len(result)} error log(s)")
        return result

    # Delegates to MonitoringService — filters logs by the given service name
    def get_logs_by_service(
        self,
        service_name: str
    ):
        logger.info(f"[STEP 1] Fetching logs for service : {service_name}")
        result = self.monitoring_service.get_logs_by_service(service_name)
        logger.info(f"[STEP 2] Retrieved {len(result)} log(s) for service : {service_name}")
        return result

    # Passes the raw query string directly to the monitoring provider for execution
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

        # Fetch all error/critical logs from the monitoring provider
        logger.info("[STEP 2] Fetching error logs from monitoring provider")
        logs = self.monitoring_service.get_error_logs()
        logger.info(f"[STEP 3] Found {len(logs)} error log(s) to process")

        # Counters to track pipeline results
        processed_logs = 0
        incidents_created = 0
        failed = 0
        skipped = 0
        incident_numbers = []
        skipped_reasons = []

        for log in logs:

            processed_logs += 1
            logger.info(f"[STEP 4.{processed_logs}] Processing log {processed_logs} of {len(logs)}")

            try:

                # Support both typed LogEntry objects and raw dicts (e.g. from New Relic GraphQL)
                if isinstance(log, LogEntry):
                    application = log.application
                    service = log.service
                    environment = log.environment
                    severity = log.severity
                    message = log.message
                    monitoring_tool = log.monitoring_tool

                else:
                    # Raw dict — use .get() with fallback defaults for missing fields
                    application = log.get("application", "Unknown")
                    service = log.get("service", "Unknown")
                    environment = log.get("environment", "Unknown")
                    severity = log.get("severity", "Unknown")
                    message = log.get("message", "No Message")
                    monitoring_tool = log.get("newrelic.source", "New Relic")

                logger.info(f"[STEP 4.{processed_logs}] Building incident | App: {application} | Service: {service} | Severity: {severity}")

                # ------------------------------------------
                # Call the Agent to analyze the log
                # Agent decides: should we create an incident?
                # ------------------------------------------
                logger.info(f"[STEP 4.{processed_logs}] Sending log to agent for analysis")

                agent_response = requests.post(
                    url=f"{Config.AGENT_URL}/agent/analyze-log",
                    json={
                        "application": application,
                        "service": service,
                        "environment": environment,
                        "severity": severity,
                        "message": message,
                        "monitoring_tool": monitoring_tool
                    },
                    timeout=30
                )

                agent_response.raise_for_status()
                agent_data = agent_response.json()

                # Agent decided to skip this log — not a system-level error
                if not agent_data.get("should_create_incident", True):
                    skipped += 1
                    reason = {
                        "application": application,
                        "service": service,
                        "error_type": agent_data.get("error_type", "Unknown"),
                        "reason": agent_data.get("reason", "No reason provided")
                    }
                    skipped_reasons.append(reason)
                    logger.info(f"[STEP 4.{processed_logs}] SKIPPED | Error Type : {reason['error_type']} | Reason : {reason['reason']}")
                    continue

                # Agent approved — use enriched fields from agent response
                logger.info(f"[STEP 4.{processed_logs}] Agent approved incident creation")

                incident = Incident(
                    short_description=agent_data.get("short_description") or message,
                    description=agent_data.get("description") or (
                        f"Application : {application}\n\n"
                        f"Service : {service}\n\n"
                        f"Environment : {environment}\n\n"
                        f"Severity : {severity}\n\n"
                        f"Message : {message}\n\n"
                        f"Generated automatically from {monitoring_tool}."
                    ),
                    category=agent_data.get("category") or "Software",
                    subcategory=agent_data.get("subcategory"),
                    business_service=service,
                    impact=agent_data.get("impact") or ("1" if severity in ("CRITICAL", "critical") else "2"),
                    urgency=agent_data.get("urgency") or ("1" if severity in ("CRITICAL", "critical") else "2"),
                )

                logger.info(f"[STEP 4.{processed_logs}] Sending incident to incident provider")

                # Submit the incident to the configured incident provider (e.g. ServiceNow)
                response = self.incident_service.create_incident(incident)

                # Extract the incident number from the provider response
                incident_number = response["result"]["number"]

                logger.info(f"[STEP 4.{processed_logs}] Incident created successfully : {incident_number}")

                incidents_created += 1
                incident_numbers.append(incident_number)

            except Exception as ex:
                # Log the failure and continue processing remaining logs
                failed += 1
                logger.error(f"[STEP 4.{processed_logs}] Failed to create incident : {ex}")

        logger.info(f"[STEP 5] Incident processing complete | Processed: {processed_logs} | Created: {incidents_created} | Skipped: {skipped} | Failed: {failed}")

        # Return a summary of the full pipeline run
        return {
            "processedLogs": processed_logs,
            "incidentsCreated": incidents_created,
            "skipped": skipped,
            "failed": failed,
            "incidentNumbers": incident_numbers,
            "skippedReasons": skipped_reasons
        }
