import requests

from config import Config
from monitoring.clients.monitoring_client import MonitoringClient
from shared.logger import get_logger

logger = get_logger("monitoring.newrelic")


class NewRelicClient(MonitoringClient):

    def __init__(self):
        logger.info("[STEP 1] Initializing New Relic client")
        self.url = "https://api.newrelic.com/graphql"
        self.account_id = int(Config.NEW_RELIC_ACCOUNT_ID)
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

        logger.info("[STEP 3] Sending request to New Relic GraphQL API")
        response = requests.post(
            url=self.url,
            headers=self.headers,
            json=payload,
            timeout=30
        )

        response.raise_for_status()
        logger.info(f"[STEP 4] Response received | Status : {response.status_code}")

        data = response.json()

        if "errors" in data:
            logger.error(f"[ERROR] New Relic returned errors : {data['errors']}")
            raise Exception(data["errors"])

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

    def get_all_logs(self):
        logger.info("[STEP 1] Executing get_all_logs query")
        query = """
        FROM Log
        SELECT *
        SINCE 1 hour ago
        LIMIT 100
        """
        return self.execute_query(query)

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

    def execute_custom_query(
        self,
        query: str
    ):
        logger.info("[STEP 1] Executing custom NRQL query")
        return self.execute_query(query)