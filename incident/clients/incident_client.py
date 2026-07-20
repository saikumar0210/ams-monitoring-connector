"""
incident/clients/incident_client.py

Abstract base class defining the interface all incident provider clients must implement.
New provider clients (ServiceNow, Jira, PagerDuty, etc.) must extend this class
and implement all abstract methods.
"""
from abc import ABC
from abc import abstractmethod

from incident.models.incident import Incident


class IncidentClient(ABC):

    @abstractmethod
    def create_incident(
        self,
        incident: Incident
    ):
        """
        Create an incident in the target incident platform.
        """
        pass

    @abstractmethod
    def update_incident(
        self,
        incident_number: str,
        payload: dict
    ):
        """
        Update an existing incident.
        """
        pass

    @abstractmethod
    def get_incident(
        self,
        incident_number: str
    ):
        """
        Retrieve an incident.
        """
        pass