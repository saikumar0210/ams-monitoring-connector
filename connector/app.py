import uvicorn

from fastapi import FastAPI

from config import Config
from connector.routes import router
from shared.logger import get_logger

logger = get_logger("connector.app")

app = FastAPI(
    title=Config.APPLICATION_NAME,
    version=Config.APPLICATION_VERSION,
    description="Generic Monitoring Connector"
)

app.include_router(router)

logger.info("[STEP 1] AMS Monitoring Connector starting up")
logger.info(f"[STEP 2] Environment        : {Config.ENVIRONMENT}")
logger.info(f"[STEP 3] Monitoring Provider : {Config.MONITORING_PROVIDER}")
logger.info(f"[STEP 4] Incident Provider   : {Config.INCIDENT_PROVIDER}")
logger.info(f"[STEP 5] Listening on        : {Config.CONNECTOR_HOST}:{Config.CONNECTOR_PORT}")


@app.get("/")
def home():

    return {
        "application": Config.APPLICATION_NAME,
        "version": Config.APPLICATION_VERSION,
        "environment": Config.ENVIRONMENT,
        "monitoringProvider": Config.MONITORING_PROVIDER,
        "incidentProvider": Config.INCIDENT_PROVIDER,
        "status": "Running"
    }


if __name__ == "__main__":

    uvicorn.run(
        "connector.app:app",
        host=Config.CONNECTOR_HOST,
        port=Config.CONNECTOR_PORT,
        reload=True
    )