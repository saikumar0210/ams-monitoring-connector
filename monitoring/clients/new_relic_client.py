"""
monitoring/clients/new_relic_client.py

Monitoring client implementation for New Relic.
Uses the New Relic GraphQL API (NerdGraph) to execute NRQL queries.

Authentication:
    API-Key header using NEW_RELIC_USER_KEY from config.

All queries target the account specified by NEW_RELIC_ACCOUNT_ID
and retrieve logs from the past 1 hour with a limit of 100 records.
"""
import requests

from config import Config
from monitoring.clients.monitoring_client import MonitoringClient
from shared.logger import get_logger

# Logger scoped to this client
logger = get_logger("monitoring.newrelic")


class NewRelicClient(MonitoringClient):

    def __init__(self):
        logger.info("[STEP 1] Initializing New Relic client")
        # NerdGraph GraphQL endpoint — single entry point for all New Relic queries
        self.url = "https://api.newrelic.com/graphql"
        # Account ID is required as a variable in every GraphQL query
        self.account_id = int(Config.NEW_RELIC_ACCOUNT_ID)
        # API-Key header authenticates the request using the user key
        self.headers = {
            "Content-Type": "application/json",
            "API-Key": Config.NEW_RELIC_USER_KEY
        }
        logger.info(f"[STEP 2] New Relic client ready | Account ID : {self.account_id}")

    # =====================================================
    # Common GraphQL Executor
    # =====================================================

    def execute_query(
        self,
        nrql: str
    ):
        logger.info(f"[STEP 1] Preparing GraphQL request to New Relic")
        logger.info(f"[STEP 2] NRQL : {nrql.strip()}")

        # Wrap the NRQL query inside the NerdGraph GraphQL structure
        # accountId and nrql are passed as variables to keep the query reusable
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

        # Build the full request payload with the query and its variables
        payload = {
            "query": graphql_query,
            "variables": {
                "accountId": self.account_id,
                "nrql": nrql.strip()
            }
        }

        logger.info("[STEP 3] Sending request to New Relic GraphQL API")
        response = requests.post(
            url=self.url,
            headers=self.headers,
            json=payload,
            timeout=30
        )

        # Raise an exception immediately for any 4xx/5xx HTTP response
        response.raise_for_status()
        logger.info(f"[STEP 4] Response received | Status : {response.status_code}")

        data = response.json()

        # New Relic returns GraphQL-level errors inside the response body even on HTTP 200
        if "errors" in data:
            logger.error(f"[ERROR] New Relic returned errors : {data['errors']}")
            raise Exception(data["errors"])

        # Navigate the nested GraphQL response to extract the results array
        results = (
            data["data"]
                ["actor"]
                ["account"]
                ["nrql"]
                ["results"]
        )
        logger.info(f"[STEP 5] Query successful - {len(results)} record(s) returned")
        return results

    # =====================================================
    # Interface Methods
    # =====================================================

    # Fetches all log types from the last 1 hour, up to 100 records
    def get_all_logs(self):
        logger.info("[STEP 1] Executing get_all_logs query")
        query = """
        FROM Log
        SELECT *
        SINCE 1 hour ago
        LIMIT 100
        """
        return self.execute_query(query)

    # Fetches only ERROR and CRITICAL logs from the last 1 hour, up to 100 records
    def get_error_logs(self):
        logger.info("[STEP 1] Executing get_error_logs query")
        query = """
        FROM Log
        SELECT *
        WHERE severity IN ('ERROR', 'CRITICAL')
        SINCE 1 hour ago
        LIMIT 100
        """
        return self.execute_query(query)

    # Fetches logs for a specific service name from the last 1 hour, up to 100 records
    def get_logs_by_service(
        self,
        service_name: str
    ):
        logger.info(f"[STEP 1] Executing get_logs_by_service query for : {service_name}")
        query = f"""
        FROM Log
        SELECT *
        WHERE service = '{service_name}'
        SINCE 1 hour ago
        LIMIT 100
        """
        return self.execute_query(query)

    # Executes a raw NRQL query string provided directly by the caller
    def execute_custom_query(
        self,
        query: str
    ):
        logger.info("[STEP 1] Executing custom NRQL query")
        return self.execute_query(query)
