from ._http_manager import _V5HTTPManager
from .spot_x import SpotX


class SpotXHTTP(_V5HTTPManager):
    def get_launchpool_project_list(self, **kwargs):
        """Get Launchpool project (activity) list

        Required args:
            status (integer): Activity phase filter.
- `0` — Upcoming
- `1` — Ongoing
- `2` — Ended

        Optional args:
            activityCoin (string): Reward coin symbol, case-insensitive.
            projectId (string): Exact activity code for a single project.
            cursor (string): Previous nextPageCursor; omit for the first page.
            limit (integer): Items per page. Default and maximum 10.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/finance/spot-x/launchpool/launchpool-project-list
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotX.GET_LAUNCHPOOL_PROJECT_LIST}",
            query=kwargs,
        )

    def get_launchpool_user_activity_log(self, **kwargs):
        """Get user's staking operation records

        Optional args:
            stakeCoin (string): Filter by stake coin symbol.
            type (integer): Operation type, from manual stake (0) through earn reward (10).
            status (integer): 0 pending, 1 success, or 2 failed.
            startTime (string): 13-digit millisecond timestamp; use with endTime.
            endTime (string): 13-digit millisecond timestamp; use with startTime.
            pageSize (integer): Records per page. Default and maximum 10.
            current (integer): One-based page. Default 1; maximum 100.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/finance/spot-x/launchpool/launchpool-activity-log
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{SpotX.GET_LAUNCHPOOL_USER_ACTIVITY_LOG}",
            query=kwargs,
            auth=True,
        )

    def get_launchpool_user_current_staking(self, **kwargs):
        """Get user's active staking positions
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/finance/spot-x/launchpool/launchpool-current-staking
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotX.GET_LAUNCHPOOL_USER_CURRENT_STAKING}",
            query=kwargs,
            auth=True,
        )

    def get_launchpool_user_history(self, **kwargs):
        """Get user's completed staking position history

        Optional args:
            stakeCoin (string): Filter by stake coin symbol.
            rewardCoin (string): Filter by reward coin symbol.
            startTime (string): Staking-start millisecond timestamp; use with endTime.
            endTime (string): Staking-end millisecond timestamp; use with startTime.
            pageSize (integer): Records per page. Default and maximum 10.
            current (integer): One-based page. Default 1; maximum 100.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/finance/spot-x/launchpool/launchpool-user-history
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{SpotX.GET_LAUNCHPOOL_USER_HISTORY}",
            query=kwargs,
            auth=True,
        )

    def get_puzzle_project_list(self, **kwargs):
        """Get Puzzle project (activity) list

        Required args:
            status (integer): Activity phase filter.
- `0` — Upcoming (not yet started)
- `1` — Ongoing (in progress)
- `2` — Ended

        Optional args:
            projectId (string): Exact activity code for a single project.
            activityCoin (string): Activity coin symbol, case-insensitive.
            cursor (string): Previous nextPageCursor; omit for the first page.
            limit (integer): Items per page. Default and maximum 10.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/finance/spot-x/puzzle/puzzle-project-list
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotX.GET_PUZZLE_PROJECT_LIST}",
            query=kwargs,
        )

    def get_token_splash_project_list(self, **kwargs):
        """Get Token Splash project (activity) list

        Required args:
            status (integer): Activity phase filter.
- `0` — Upcoming (registration not yet started)
- `1` — Ongoing (activity in progress)
- `2` — Ended (announcement time has passed)

        Optional args:
            projectId (string): Exact activity code for a single project.
            activityCoin (string): Activity coin symbol, case-insensitive.
            cursor (string): Previous nextPageCursor; omit for the first page.
            limit (integer): Items per page. Default and maximum 10.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/finance/spot-x/token-splash/token-splash-project-list
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotX.GET_TOKEN_SPLASH_PROJECT_LIST}",
            query=kwargs,
        )

    def get_token_splash_user_activity_params(self, **kwargs):
        """Get user's Token Splash trade-task progress

        Optional args:
            projectId (string): Exact activity code for a single project.
            activityCoin (string): Activity coin symbol, case-insensitive.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/finance/spot-x/token-splash/token-splash-user-activity-params
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{SpotX.GET_TOKEN_SPLASH_USER_ACTIVITY_PARAMS}",
            query=kwargs,
            auth=True,
        )
