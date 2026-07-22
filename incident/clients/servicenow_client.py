"""
incident/clients/servicenow_client.py

Incident client implementation for ServiceNow.
Uses the ServiceNow REST API (Table API) to manage incidents.

Authentication:
    Basic auth using SERVICENOW_USERNAME and SERVICENOW_PASSWORD from config.

Target table:
    /api/now/table/incident
"""
import json
import requests

from config import Config
from incident.clients.incident_client import IncidentClient
from incident.models.incident import Incident
from shared.logger import get_logger

# Logger scoped to this client
logger = get_logger("incident.servicenow")


class ServiceNowClient(IncidentClient):

    def __init__(self):
        logger.info("[STEP 1] Initializing ServiceNow client")
        # Build the full Table API URL targeting the incident table
        self.base_url = (
            f"https://{Config.SERVICENOW_INSTANCE}"
            "/api/now/table/incident"
        )
        # Basic auth credentials passed with every request
        self.auth = (
            Config.SERVICENOW_USERNAME,
            Config.SERVICENOW_PASSWORD
        )
        # Standard headers required by the ServiceNow REST API
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        logger.info(f"[STEP 2] ServiceNow client ready | Instance : {Config.SERVICENOW_INSTANCE}")

    # =====================================================
    # Create Incident
    # =====================================================

    def create_incident(
        self,
        incident: Incident
    ):
        logger.info("[STEP 1] Building ServiceNow incident payload")

        # Map Incident model fields to ServiceNow Table API field names
        payload = {
            "short_description": incident.short_description,  # Incident title
            "description": incident.description,              # Full incident details
            "category": incident.category,                    # e.g. Software
            "subcategory": incident.subcategory,
            "business_service": incident.business_service,    # Affected service
            "service_offering": incident.service_offering,    # Service offering
            "cmdb_ci": incident.cmdb_ci,                      # Configuration item
            "impact": incident.impact,                        # 1=High, 2=Medium, 3=Low
            "urgency": incident.urgency,                      # 1=High, 2=Medium, 3=Low
            "state": incident.state,                          # 1=New
            "contact_type": incident.contact_type,            # Channel e.g. email, api
            "assignment_group": incident.assignment_group,
            "assigned_to": incident.assigned_to,
            "caller_id": incident.caller_id,
        }

        # Strip out None values — ServiceNow treats missing fields as unset
        payload = {k: v for k, v in payload.items() if v is not None}

        logger.info(f"[STEP 2] Sending POST request to ServiceNow | URL : {self.base_url}")

        # POST to the incident table to create a new record
        response = requests.post(
            url=self.base_url,
            headers=self.headers,
            auth=self.auth,
            json=payload,
            timeout=30
        )

        logger.info(f"[STEP 3] Response received | Status : {response.status_code}")

        # Any non-2xx response is treated as a failure
        if not response.ok:
            logger.error(f"[ERROR] ServiceNow API error | Status : {response.status_code} | Response : {response.text}")
            raise Exception(
                f"""
ServiceNow API Error

Status Code : {response.status_code}

Response :

{response.text}
"""
            )

        response_json = response.json()

        # ServiceNow always wraps successful responses in a "result" key
        if "result" not in response_json:
            logger.error(f"[ERROR] Unexpected ServiceNow response : {json.dumps(response_json, indent=4)}")
            raise Exception(
                f"""
Unexpected ServiceNow Response

{json.dumps(response_json, indent=4)}
"""
            )

        logger.info(f"[STEP 4] Incident created in ServiceNow | Number : {response_json['result'].get('number')}")
        return response_json

    # =====================================================
    # Update Incident
    # =====================================================

    def update_incident(
        self,
        incident_number: str,
        payload: dict
    ):
        logger.info(f"[STEP 1] Sending PATCH request to ServiceNow | Incident : {incident_number}")
        # PATCH updates only the fields provided in the payload, leaving others unchanged
        response = requests.patch(
            url=f"{self.base_url}/{incident_number}",
            headers=self.headers,
            auth=self.auth,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        logger.info(f"[STEP 2] Incident updated | Status : {response.status_code}")
        return response.json()

    # =====================================================
    # Get Incident
    # =====================================================

    def get_incident(
        self,
        incident_number: str
    ):
        logger.info(f"[STEP 1] Sending GET request to ServiceNow | Incident : {incident_number}")
        # GET retrieves the full incident record by its sys_id or number
        response = requests.get(
            url=f"{self.base_url}/{incident_number}",
            headers=self.headers,
            auth=self.auth,
            timeout=30
        )
        response.raise_for_status()
        logger.info(f"[STEP 2] Incident retrieved | Status : {response.status_code}")
        return response.json()
