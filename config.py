import os

from dotenv import load_dotenv

load_dotenv()


class Config:

    # =====================================================
    # Application
    # =====================================================

    APPLICATION_NAME = os.getenv(
        "APPLICATION_NAME",
        "AMS Monitoring Connector"
    )

    APPLICATION_VERSION = os.getenv(
        "APPLICATION_VERSION",
        "1.0.0"
    )

    ENVIRONMENT = os.getenv(
        "ENVIRONMENT",
        "DEV"
    )

    # =====================================================
    # Connector
    # =====================================================

    CONNECTOR_HOST = os.getenv(
        "CONNECTOR_HOST",
        "0.0.0.0"
    )

    CONNECTOR_PORT = int(
        os.getenv(
            "CONNECTOR_PORT",
            "8000"
        )
    )

    # =====================================================
    # Monitoring Provider
    # =====================================================

    MONITORING_PROVIDER = os.getenv(
        "MONITORING_PROVIDER",
        "NEW_RELIC"
    ).upper()

    # =====================================================
    # Incident Provider
    # =====================================================

    INCIDENT_PROVIDER = os.getenv(
        "INCIDENT_PROVIDER",
        "SERVICENOW"
    ).upper()

    # =====================================================
    # New Relic
    # =====================================================

    NEW_RELIC_ACCOUNT_ID = os.getenv(
        "NEW_RELIC_ACCOUNT_ID"
    )

    NEW_RELIC_USER_KEY = os.getenv(
        "NEW_RELIC_USER_KEY"
    )

    NEW_RELIC_LICENSE_KEY = os.getenv(
        "NEW_RELIC_LICENSE_KEY"
    )

    NEW_RELIC_REGION = os.getenv(
        "NEW_RELIC_REGION",
        "US"
    )

    # =====================================================
    # Datadog
    # =====================================================

    DATADOG_API_KEY = os.getenv(
        "DATADOG_API_KEY"
    )

    DATADOG_APP_KEY = os.getenv(
        "DATADOG_APP_KEY"
    )

    DATADOG_SITE = os.getenv(
        "DATADOG_SITE",
        "datadoghq.com"
    )

    # =====================================================
    # Splunk
    # =====================================================

    SPLUNK_HOST = os.getenv(
        "SPLUNK_HOST"
    )

    SPLUNK_PORT = os.getenv(
        "SPLUNK_PORT"
    )

    SPLUNK_USERNAME = os.getenv(
        "SPLUNK_USERNAME"
    )

    SPLUNK_PASSWORD = os.getenv(
        "SPLUNK_PASSWORD"
    )

    SPLUNK_HEC_TOKEN = os.getenv(
        "SPLUNK_HEC_TOKEN"
    )

    # =====================================================
    # Grafana
    # =====================================================

    GRAFANA_URL = os.getenv(
        "GRAFANA_URL"
    )

    GRAFANA_TOKEN = os.getenv(
        "GRAFANA_TOKEN"
    )

    # =====================================================
    # ServiceNow
    # =====================================================

    SERVICENOW_INSTANCE = os.getenv(
        "SERVICENOW_INSTANCE"
    )

    SERVICENOW_USERNAME = os.getenv(
        "SERVICENOW_USERNAME"
    )

    SERVICENOW_PASSWORD = os.getenv(
        "SERVICENOW_PASSWORD"
    )