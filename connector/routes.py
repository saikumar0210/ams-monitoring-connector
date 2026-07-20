"""
connector/routes.py

Defines all API routes for the AMS Monitoring Connector.

Endpoints:
    GET  /api/logs                     - Fetch all logs from the monitoring provider
    GET  /api/logs/errors              - Fetch only error/critical logs
    GET  /api/logs/service/{name}      - Fetch logs filtered by service name
    POST /api/logs/query               - Execute a custom provider-specific query
    POST /api/process-incidents        - Fetch error logs and create incidents in the incident platform
"""
from fastapi import APIRouter

from connector.models import (
    CustomQueryRequest,
    ProcessIncidentRequest
)

from connector.services.monitoring_connector_service import (
    MonitoringConnectorService
)
from shared.logger import get_logger

# Logger scoped to this module for request/response tracing
logger = get_logger("connector.routes")

# All routes are grouped under /api with a shared tag for Swagger UI
router = APIRouter(
    prefix="/api",
    tags=["Monitoring Connector"]
)

# Single shared service instance used by all route handlers
connector_service = MonitoringConnectorService()


# =====================================================
# Logs
# =====================================================

# Returns all logs from the configured monitoring provider (last 1 hour)
@router.get("/logs")
def get_all_logs():
    logger.info("[REQUEST] GET /api/logs - Fetching all logs")
    result = connector_service.get_all_logs()
    logger.info(f"[RESPONSE] GET /api/logs - Returned {len(result)} log(s)")
    return result


# Returns only ERROR and CRITICAL severity logs from the monitoring provider
@router.get("/logs/errors")
def get_error_logs():
    logger.info("[REQUEST] GET /api/logs/errors - Fetching error logs")
    result = connector_service.get_error_logs()
    logger.info(f"[RESPONSE] GET /api/logs/errors - Returned {len(result)} error log(s)")
    return result


# Returns logs filtered by a specific service name passed as a path parameter
@router.get("/logs/service/{service_name}")
def get_logs_by_service(
    service_name: str
):
    logger.info(f"[REQUEST] GET /api/logs/service/{service_name} - Fetching logs for service")
    result = connector_service.get_logs_by_service(service_name)
    logger.info(f"[RESPONSE] GET /api/logs/service/{service_name} - Returned {len(result)} log(s)")
    return result


# Accepts a raw NRQL/provider query string and executes it directly against the monitoring provider
@router.post("/logs/query")
def execute_custom_query(
    request: CustomQueryRequest
):
    logger.info(f"[REQUEST] POST /api/logs/query - Query : {request.query}")
    result = connector_service.execute_custom_query(request.query)
    logger.info(f"[RESPONSE] POST /api/logs/query - Returned {len(result)} result(s)")
    return result


# =====================================================
# Incident Processing
# =====================================================

# Triggers the full pipeline: fetch error logs → map to incidents → create in incident platform
@router.post("/process-incidents")
def process_incidents(
    request: ProcessIncidentRequest
):
    logger.info("[REQUEST] POST /api/process-incidents - Starting incident processing")
    result = connector_service.process_incidents(request)
    logger.info(f"[RESPONSE] POST /api/process-incidents - Processed: {result['processedLogs']} | Created: {result['incidentsCreated']} | Failed: {result['failed']}")
    return result
