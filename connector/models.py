"""
connector/models.py

Request models for the Connector API endpoints.

Models:
    CustomQueryRequest      - Payload for POST /api/logs/query
    ProcessIncidentRequest  - Payload for POST /api/process-incidents
"""
from pydantic import BaseModel


# Request body for POST /api/logs/query
# Accepts a raw query string to be executed directly against the monitoring provider
class CustomQueryRequest(BaseModel):

    query: str  # Provider-specific query e.g. NRQL for New Relic


# Request body for POST /api/process-incidents
# Both fields are optional filters — if omitted, all error logs are processed
class ProcessIncidentRequest(BaseModel):

    service_name: str | None = None  # Filter incidents to a specific service

    severity: str | None = None      # Filter incidents to a specific severity level
