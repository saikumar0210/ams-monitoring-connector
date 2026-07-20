"""
monitoring/clients/monitoring_client.py

Abstract base class defining the interface all monitoring provider clients must implement.
New provider clients (New Relic, Datadog, Splunk, etc.) must extend this class
and implement all abstract methods.
"""
from abc import ABC
from abc import abstractmethod


class MonitoringClient(ABC):

    @abstractmethod
    def get_all_logs(self):
        """
        Fetch all logs from the monitoring platform.
        """
        pass

    @abstractmethod
    def get_error_logs(self):
        """
        Fetch only ERROR logs.
        """
        pass

    @abstractmethod
    def get_logs_by_service(
        self,
        service_name: str
    ):
        """
        Fetch logs for a specific application/service.
        """
        pass

    @abstractmethod
    def execute_custom_query(
        self,
        query: str
    ):
        """
        Execute a provider-specific query.
        """
        pass