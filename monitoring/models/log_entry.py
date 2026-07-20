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