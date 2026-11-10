from enum import Enum


class Referral(str, Enum):
    GET_REFERRAL_CAMPAIGN_REWARDS = "/v5/referral/campaign/rewards"
    GET_REFERRAL_COMMISSION_RECORDS = "/v5/referral/commission/records"
    GET_REFERRAL_USER_IDENTITY_PROFILE = "/v5/referral/user/identity-profile"
    GET_REFERRAL_USER_INVITATIONS = "/v5/referral/user/invitations"
    def __str__(self) -> str:
        return self.value
