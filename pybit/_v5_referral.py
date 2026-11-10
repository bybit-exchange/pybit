from ._http_manager import _V5HTTPManager
from .referral import Referral


class ReferralHTTP(_V5HTTPManager):
    def get_referral_campaign_rewards(self, **kwargs):
        """Get referral rules and campaign task rewards for the current site
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/referral/referral-campaign-rewards
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Referral.GET_REFERRAL_CAMPAIGN_REWARDS}",
            query=kwargs,
            auth=True,
        )

    def get_referral_commission_records(self, **kwargs):
        """Get Referral Commission Records
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/referral/referral-commission-records
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Referral.GET_REFERRAL_COMMISSION_RECORDS}",
            query=kwargs,
            auth=True,
        )

    def get_referral_user_identity_profile(self, **kwargs):
        """Get Referral User Identity Profile
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/referral/referral-user-identity-profile
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Referral.GET_REFERRAL_USER_IDENTITY_PROFILE}",
            query=kwargs,
            auth=True,
        )

    def get_referral_user_invitations(self, **kwargs):
        """Get referral user invitations
        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/referral/referral-user-invitations
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Referral.GET_REFERRAL_USER_INVITATIONS}",
            query=kwargs,
            auth=True,
        )
