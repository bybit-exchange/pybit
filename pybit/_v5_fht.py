from ._http_manager import _V5HTTPManager
from .fht import FHT


class FHTHTTP(_V5HTTPManager):
    def batch_create_tax_reports(self, **kwargs):
        """Batch request export reports.

        Required args:
            startTime (integer): Report start time. UNIX timestamp in seconds, within the last 18 months.
            endTime (integer): Report end time. UNIX timestamp in seconds. Must be later than startTime, with a time range of at most 12 months.
            items (array): List of report objects to export. At least one item is required.

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
        """Get batch export report status.

        Required args:
            batchId (string): Batch ID in UUID format, returned by Batch Request Export Reports.

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
