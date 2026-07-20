"""
monitoring/models/log_entry.py

Pydantic model representing a normalized log entry retrieved from a monitoring provider.
All monitoring clients map their provider-specific response into this structure.

Fields:
    monitoring_tool - Name of the monitoring provider (e.g. New Relic, Datadog)
    application     - Name of the application that generated the log
    service         - Specific service or component within the application
    environment     - Deployment environment (e.g. production, staging)
    severity        - Log severity level (e.g. ERROR, CRITICAL, INFO)
    message         - Human-readable log message
    timestamp       - UTC datetime when the log was generated
    raw_payload     - Original unmodified response from the monitoring provider
"""
from datetime import datetime

from pydantic import BaseModel


class LogEntry(BaseModel):

    monitoring_tool: str

    application: str

    service: str

    environment: str

    severity: str

    message: str

    timestamp: datetime

    raw_payload: dict