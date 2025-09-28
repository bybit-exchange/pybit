from ._http_manager import _V5HTTPManager
from .rate_limit import RateLimit


class RateLimitHTTP(_V5HTTPManager):
    def set_api_rate_limit(self, **kwargs):
        """
        Required args:
            list (array): An array of objects
            > uids (string): Multiple UIDs, separated by commas
            > bizType (string): Business type
            > rate (integer): API rate limit per second
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rate-limit
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{RateLimit.SET_API_RATE_LIMIT}",
            query=kwargs,
            auth=True,
        )

    def get_api_rate_limit(self, **kwargs):
        """
        Required args:
            uids (string): Multiple UIDs, separated by commas

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rate-limit
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{RateLimit.GET_API_RATE_LIMIT}",
            query=kwargs,
            auth=True,
        )

    def get_api_rate_limit_cap(self):
        """
        Required args:
            None

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rate-limit
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{RateLimit.GET_API_RATE_LIMIT_CAP}",
            auth=True,
        )

    def get_all_api_rate_limits(self, **kwargs):
        """
        Get all your account's API rate limits (master and subaccounts).
        Required args:
            None

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/rate-limit
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{RateLimit.GET_ALL_API_RATE_LIMITS}",
            query=kwargs,
            auth=True,
        )
