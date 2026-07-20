from fastapi import APIRouter

from connector.models import (
    CustomQueryRequest,
    ProcessIncidentRequest
)

from connector.services.monitoring_connector_service import (
    MonitoringConnectorService
)

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

    return connector_service.get_all_logs()


@router.get("/logs/errors")
def get_error_logs():

    return connector_service.get_error_logs()


@router.get("/logs/service/{service_name}")
def get_logs_by_service(
    service_name: str
):

    return connector_service.get_logs_by_service(
        service_name
    )


@router.post("/logs/query")
def execute_custom_query(
    request: CustomQueryRequest
):

    return connector_service.execute_custom_query(
        request.query
    )


# =====================================================
# Incident Processing
# =====================================================

@router.post("/process-incidents")
def process_incidents(
    request: ProcessIncidentRequest
):

    return connector_service.process_incidents(
        request
    )