from ._http_manager import _V5HTTPManager
from .fht import FHT


class FHTHTTP(_V5HTTPManager):
    def batch_create_tax_reports(self, **kwargs):
        """Batch create tax report files.

        Required args:
            startTime (integer): Tax report start time (Unix timestamp, seconds)
            endTime (integer): Tax report end time (Unix timestamp, seconds); interval must not exceed 12 months
            items (array): Non-empty list of tax report export items

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/tax/batch-create
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{FHT.BATCH_CREATE_TAX_REPORTS}",
            query=kwargs,
            auth=True,
        )

    def batch_query_tax_reports(self, **kwargs):
        """Query batch tax report status.

        Required args:
            batchId (string): Batch ID returned by `batch_create`

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/tax/batch-query
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{FHT.BATCH_QUERY_TAX_REPORTS}",
            query=kwargs,
            auth=True,
        )
