import uvicorn

from fastapi import FastAPI

from config import Config
from connector.routes import router


app = FastAPI(
    title=Config.APPLICATION_NAME,
    version=Config.APPLICATION_VERSION,
    description="Generic Monitoring Connector"
)

app.include_router(router)


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