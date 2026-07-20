import json
import requests

from config import Config
from incident.clients.incident_client import IncidentClient
from incident.models.incident import Incident
from shared.logger import get_logger

logger = get_logger("incident.servicenow")


class ServiceNowClient(IncidentClient):

    def __init__(self):
        logger.info("[STEP 1] Initializing ServiceNow client")
        self.base_url = (
            f"https://{Config.SERVICENOW_INSTANCE}"
            "/api/now/table/incident"
        )
        self.auth = (
            Config.SERVICENOW_USERNAME,
            Config.SERVICENOW_PASSWORD
        )
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

        payload = {
            "short_description": incident.short_description,
            "description": incident.description,
            "category": incident.category,
            "subcategory": incident.subcategory,
            "business_service": incident.business_service,
            "impact": incident.impact,
            "urgency": incident.urgency,
            "state": incident.state,
            "contact_type": incident.contact_type,
            "assignment_group": incident.assignment_group,
            "assigned_to": incident.assigned_to,
            "caller_id": incident.caller_id,
        }

        # Remove None values — ServiceNow ignores missing fields cleanly
        payload = {k: v for k, v in payload.items() if v is not None}

        logger.info(f"[STEP 2] Sending POST request to ServiceNow | URL : {self.base_url}")

        response = requests.post(
            url=self.base_url,
            headers=self.headers,
            auth=self.auth,
            json=payload,
            timeout=30
        )

        logger.info(f"[STEP 3] Response received | Status : {response.status_code}")

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

    def get_incident(
        self,
        incident_number: str
    ):
        logger.info(f"[STEP 1] Sending GET request to ServiceNow | Incident : {incident_number}")
        response = requests.get(
            url=f"{self.base_url}/{incident_number}",
            headers=self.headers,
            auth=self.auth,
            timeout=30
        )
        response.raise_for_status()
        logger.info(f"[STEP 2] Incident retrieved | Status : {response.status_code}")
        return response.json()