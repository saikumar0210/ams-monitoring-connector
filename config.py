"""
config.py

Centralized configuration for the AMS Monitoring Connector.
All values are loaded from environment variables with sensible defaults.

Sections:
    Application     - App name, version, environment
    Connector       - Host and port for the FastAPI server
    Monitoring      - Active monitoring provider (NEW_RELIC, DATADOG, SPLUNK, GRAFANA, ELASTIC)
    Incident        - Active incident provider (SERVICENOW, JIRA, PAGERDUTY, OPSGENIE)
    New Relic       - Account ID, user key, license key, region
    Datadog         - API key, app key, site
    Splunk          - Host, port, credentials, HEC token
    Grafana         - URL, token
    ServiceNow      - Instance URL, username, password
"""
import os

from dotenv import load_dotenv

# Load variables from .env file into the environment (no-op if already set)
load_dotenv()


class Config:

    # =====================================================
    # Application
    # =====================================================

    # Display name shown in Swagger UI and health check response
    APPLICATION_NAME = os.getenv(
        "APPLICATION_NAME",
        "AMS Monitoring Connector"
    )

    # Semantic version of the application
    APPLICATION_VERSION = os.getenv(
        "APPLICATION_VERSION",
        "1.0.0"
    )

    # Deployment environment label e.g. DEV, STAGING, PROD
    ENVIRONMENT = os.getenv(
        "ENVIRONMENT",
        "DEV"
    )

    # =====================================================
    # Connector
    # =====================================================

    # Host the FastAPI server binds to — 0.0.0.0 allows external access
    CONNECTOR_HOST = os.getenv(
        "CONNECTOR_HOST",
        "0.0.0.0"
    )

    # Port the FastAPI server listens on
    CONNECTOR_PORT = int(
        os.getenv(
            "CONNECTOR_PORT",
            "8000"
        )
    )

    # =====================================================
    # Monitoring Provider
    # =====================================================

    # Determines which monitoring client is instantiated by MonitoringClientFactory
    # Supported values: NEW_RELIC, DATADOG, SPLUNK, GRAFANA, ELASTIC
    MONITORING_PROVIDER = os.getenv(
        "MONITORING_PROVIDER",
        "NEW_RELIC"
    ).upper()

    # =====================================================
    # Incident Provider
    # =====================================================

    # Determines which incident client is instantiated by IncidentClientFactory
    # Supported values: SERVICENOW, JIRA, PAGERDUTY, OPSGENIE
    INCIDENT_PROVIDER = os.getenv(
        "INCIDENT_PROVIDER",
        "SERVICENOW"
    ).upper()

    # =====================================================
    # New Relic
    # =====================================================

    # Numeric account ID used in all NerdGraph GraphQL queries
    NEW_RELIC_ACCOUNT_ID = os.getenv(
        "NEW_RELIC_ACCOUNT_ID"
    )

    # User API key used in the API-Key request header for NerdGraph
    NEW_RELIC_USER_KEY = os.getenv(
        "NEW_RELIC_USER_KEY"
    )

    # License/ingest key used for sending data to New Relic
    NEW_RELIC_LICENSE_KEY = os.getenv(
        "NEW_RELIC_LICENSE_KEY"
    )

    # Region of the New Relic account — US or EU
    NEW_RELIC_REGION = os.getenv(
        "NEW_RELIC_REGION",
        "US"
    )

    # =====================================================
    # Datadog
    # =====================================================

    # Datadog API key for authenticating requests
    DATADOG_API_KEY = os.getenv(
        "DATADOG_API_KEY"
    )

    # Datadog application key for authorizing specific operations
    DATADOG_APP_KEY = os.getenv(
        "DATADOG_APP_KEY"
    )

    # Datadog site endpoint e.g. datadoghq.com or datadoghq.eu
    DATADOG_SITE = os.getenv(
        "DATADOG_SITE",
        "datadoghq.com"
    )

    # =====================================================
    # Splunk
    # =====================================================

    # Hostname or IP of the Splunk instance
    SPLUNK_HOST = os.getenv(
        "SPLUNK_HOST"
    )

    # Port Splunk is listening on (default 8089 for REST API)
    SPLUNK_PORT = os.getenv(
        "SPLUNK_PORT"
    )

    # Splunk admin username for basic auth
    SPLUNK_USERNAME = os.getenv(
        "SPLUNK_USERNAME"
    )

    # Splunk admin password for basic auth
    SPLUNK_PASSWORD = os.getenv(
        "SPLUNK_PASSWORD"
    )

    # HTTP Event Collector token for sending events to Splunk
    SPLUNK_HEC_TOKEN = os.getenv(
        "SPLUNK_HEC_TOKEN"
    )

    # =====================================================
    # Grafana
    # =====================================================

    # Base URL of the Grafana instance e.g. https://grafana.example.com
    GRAFANA_URL = os.getenv(
        "GRAFANA_URL"
    )

    # Grafana service account token for API authentication
    GRAFANA_TOKEN = os.getenv(
        "GRAFANA_TOKEN"
    )

    # =====================================================
    # ServiceNow
    # =====================================================

    # ServiceNow instance subdomain e.g. dev12345.service-now.com
    SERVICENOW_INSTANCE = os.getenv(
        "SERVICENOW_INSTANCE"
    )

    # ServiceNow username for basic auth
    SERVICENOW_USERNAME = os.getenv(
        "SERVICENOW_USERNAME"
    )

    # ServiceNow password for basic auth
    SERVICENOW_PASSWORD = os.getenv(
        "SERVICENOW_PASSWORD"
    )

    # =====================================================
    # Agent
    # =====================================================

    # URL of the AMS Incident Agent service
    # Locally: http://localhost:8001
    # Production: https://ams-incident-agent.onrender.com
    AGENT_URL = os.getenv(
        "AGENT_URL",
        "http://localhost:8001"
    )
