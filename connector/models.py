from pydantic import BaseModel


class CustomQueryRequest(BaseModel):

    query: str


class ProcessIncidentRequest(BaseModel):

    service_name: str | None = None

    severity: str | None = None