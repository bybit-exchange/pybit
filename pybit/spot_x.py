from enum import Enum


class SpotX(str, Enum):
    GET_LAUNCHPOOL_PROJECT_LIST = "/v5/spot-x/launchpool/project/list"
    GET_LAUNCHPOOL_USER_ACTIVITY_LOG = "/v5/spot-x/launchpool/user/activity-log"
    GET_LAUNCHPOOL_USER_CURRENT_STAKING = "/v5/spot-x/launchpool/user/current-staking"
    GET_LAUNCHPOOL_USER_HISTORY = "/v5/spot-x/launchpool/user/history"
    GET_PUZZLE_PROJECT_LIST = "/v5/spot-x/puzzle/project/list"
    GET_TOKEN_SPLASH_PROJECT_LIST = "/v5/spot-x/token-splash/project/list"
    GET_TOKEN_SPLASH_USER_ACTIVITY_PARAMS = "/v5/spot-x/token-splash/user/activity-params"
    def __str__(self) -> str:
        return self.value
