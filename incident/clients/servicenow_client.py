import json
import requests

from config import Config
from incident.clients.incident_client import IncidentClient
from incident.models.incident import Incident


class ServiceNowClient(IncidentClient):

    def __init__(self):

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

    # =====================================================
    # Create Incident
    # =====================================================

    def create_incident(
        self,
        incident: Incident
    ):

        payload = {

            "short_description": incident.title,

            "description": incident.description,

            "category": "Software",

            "impact": "2",

            "urgency": "2"
        }

        print("\n" + "=" * 80)
        print("Creating ServiceNow Incident")
        print("=" * 80)
        print("URL:")
        print(self.base_url)

        print("\nPayload:")
        print(json.dumps(payload, indent=4))

        response = requests.post(
            url=self.base_url,
            headers=self.headers,
            auth=self.auth,
            json=payload,
            timeout=30
        )

        print("\nStatus Code:")
        print(response.status_code)

        print("\nResponse:")
        print(response.text)

        print("=" * 80)

        if not response.ok:

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

            raise Exception(
                f"""
Unexpected ServiceNow Response

{json.dumps(response_json, indent=4)}
"""
            )

        return response_json

    # =====================================================
    # Update Incident
    # =====================================================

    def update_incident(
        self,
        incident_number: str,
        payload: dict
    ):

        response = requests.patch(
            url=f"{self.base_url}/{incident_number}",
            headers=self.headers,
            auth=self.auth,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    # =====================================================
    # Get Incident
    # =====================================================

    def get_incident(
        self,
        incident_number: str
    ):

        response = requests.get(
            url=f"{self.base_url}/{incident_number}",
            headers=self.headers,
            auth=self.auth,
            timeout=30
        )

        response.raise_for_status()

        return response.json()