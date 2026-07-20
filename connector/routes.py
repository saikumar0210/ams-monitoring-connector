from fastapi import APIRouter

from connector.models import (
    CustomQueryRequest,
    ProcessIncidentRequest
)

from connector.services.monitoring_connector_service import (
    MonitoringConnectorService
)
from shared.logger import get_logger

logger = get_logger("connector.routes")

router = APIRouter(
    prefix="/api",
    tags=["Monitoring Connector"]
)

connector_service = MonitoringConnectorService()


# =====================================================
# Logs
# =====================================================

@router.get("/logs")
def get_all_logs():
    logger.info("[REQUEST] GET /api/logs - Fetching all logs")
    result = connector_service.get_all_logs()
    logger.info(f"[RESPONSE] GET /api/logs - Returned {len(result)} log(s)")
    return result


@router.get("/logs/errors")
def get_error_logs():
    logger.info("[REQUEST] GET /api/logs/errors - Fetching error logs")
    result = connector_service.get_error_logs()
    logger.info(f"[RESPONSE] GET /api/logs/errors - Returned {len(result)} error log(s)")
    return result


@router.get("/logs/service/{service_name}")
def get_logs_by_service(
    service_name: str
):
    logger.info(f"[REQUEST] GET /api/logs/service/{service_name} - Fetching logs for service")
    result = connector_service.get_logs_by_service(service_name)
    logger.info(f"[RESPONSE] GET /api/logs/service/{service_name} - Returned {len(result)} log(s)")
    return result


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

@router.post("/process-incidents")
def process_incidents(
    request: ProcessIncidentRequest
):
    logger.info("[REQUEST] POST /api/process-incidents - Starting incident processing")
    result = connector_service.process_incidents(request)
    logger.info(f"[RESPONSE] POST /api/process-incidents - Processed: {result['processedLogs']} | Created: {result['incidentsCreated']} | Failed: {result['failed']}")
    return result