import requests

from config import Config
from monitoring.clients.monitoring_client import MonitoringClient


class NewRelicClient(MonitoringClient):

    def __init__(self):

        self.url = "https://api.newrelic.com/graphql"

        self.account_id = int(
            Config.NEW_RELIC_ACCOUNT_ID
        )

        self.headers = {
            "Content-Type": "application/json",
            "API-Key": Config.NEW_RELIC_USER_KEY
        }

    # =====================================================
    # Common GraphQL Executor
    # =====================================================

    def execute_query(
        self,
        nrql: str
    ):

        graphql_query = """
        query($accountId: Int!, $nrql: Nrql!) {
          actor {
            account(id: $accountId) {
              nrql(query: $nrql) {
                results
              }
            }
          }
        }
        """

        payload = {
            "query": graphql_query,
            "variables": {
                "accountId": self.account_id,
                "nrql": nrql.strip()
            }
        }

        response = requests.post(
            url=self.url,
            headers=self.headers,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        if "errors" in data:
            raise Exception(data["errors"])

        return (
            data["data"]
                ["actor"]
                ["account"]
                ["nrql"]
                ["results"]
        )

    # =====================================================
    # Interface Methods
    # =====================================================

    def get_all_logs(self):

        query = """
        FROM Log
        SELECT *
        SINCE 1 hour ago
        LIMIT 100
        """

        return self.execute_query(query)

    def get_error_logs(self):

        query = """
        FROM Log
        SELECT *
        WHERE severity IN ('ERROR', 'CRITICAL')
        SINCE 1 hour ago
        LIMIT 100
        """

        return self.execute_query(query)

    def get_logs_by_service(
        self,
        service_name: str
    ):

        query = f"""
        FROM Log
        SELECT *
        WHERE service = '{service_name}'
        SINCE 1 hour ago
        LIMIT 100
        """

        return self.execute_query(query)

    def execute_custom_query(
        self,
        query: str
    ):

        return self.execute_query(query)