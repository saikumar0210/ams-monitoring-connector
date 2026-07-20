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

        return self.monitoring_service.get_all_logs()

    def get_error_logs(self):

        return self.monitoring_service.get_error_logs()

    def get_logs_by_service(
        self,
        service_name: str
    ):

        return self.monitoring_service.get_logs_by_service(
            service_name
        )

    def execute_custom_query(
        self,
        query: str
    ):

        return self.monitoring_service.execute_custom_query(
            query
        )

    # =====================================================
    # Process Incidents
    # =====================================================

    def process_incidents(
        self,
        request: ProcessIncidentRequest
    ):

        logs = self.monitoring_service.get_error_logs()

        processed_logs = 0

        incidents_created = 0

        failed = 0

        incident_numbers = []

        for log in logs:

            processed_logs += 1

            try:

                # ------------------------------------------
                # Handle LogEntry object or dictionary
                # ------------------------------------------

                if isinstance(log, LogEntry):

                    application = log.application
                    service = log.service
                    environment = log.environment
                    severity = log.severity
                    message = log.message
                    monitoring_tool = log.monitoring_tool

                else:

                    application = log.get(
                        "application",
                        "Unknown"
                    )

                    service = log.get(
                        "service",
                        "Unknown"
                    )

                    environment = log.get(
                        "environment",
                        "Unknown"
                    )

                    severity = log.get(
                        "severity",
                        "Unknown"
                    )

                    message = log.get(
                        "message",
                        "No Message"
                    )

                    monitoring_tool = log.get(
                        "newrelic.source",
                        "New Relic"
                    )

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

                print("=" * 60)
                print("Creating ServiceNow Incident")
                print(f"Title : {incident.title}")
                print(f"Severity : {incident.severity}")
                print("=" * 60)

                response = (
                    self.incident_service.create_incident(
                        incident
                    )
                )

                incident_number = (
                    response["result"]["number"]
                )

                print(
                    f"Incident Created : {incident_number}"
                )

                incidents_created += 1

                incident_numbers.append(
                    incident_number
                )

            except Exception as ex:

                failed += 1

                print("=" * 60)
                print("Incident Creation Failed")
                print(ex)
                print("=" * 60)

        return {

            "processedLogs": processed_logs,

            "incidentsCreated": incidents_created,

            "failed": failed,

            "incidentNumbers": incident_numbers
        }