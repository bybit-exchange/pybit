from ._http_manager import _V5HTTPManager
from .user import User


class UserHTTP(_V5HTTPManager):
    def create_sub_uid(self, **kwargs):
        """Create a new sub user id. Use master user's api key only.

        Required args:
            username (string): Give a username of the new sub user id. 6-16 characters, must include both numbers and letters.cannot be the same as the exist or deleted one.
            memberType (integer): 1: normal sub account, 6: custodial sub account

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/user/create-subuid
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{User.CREATE_SUB_UID}",
            query=kwargs,
            auth=True,
        )

    def create_sub_api_key(self, **kwargs):
        """To create new API key for those newly created sub UID. Use master user's api key only.

        Required args:
            subuid (integer): Sub user Id
            readOnly (integer): 0: Read and Write. 1: Read only
            permissions (Object): Tick the types of permission. one of below types must be passed, otherwise the error is thrown

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/user/create-subuid-apikey
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{User.CREATE_SUB_API_KEY}",
            query=kwargs,
            auth=True,
        )

    def get_sub_uid_list(self, **kwargs):
        """Get all sub uid of master account. Use master user's api key only.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/user/subuid-list
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{User.GET_SUB_UID_LIST}",
            query=kwargs,
            auth=True,
        )

    def freeze_sub_uid(self, **kwargs):
        """Froze sub uid. Use master user's api key only.

        Required args:
            subuid (integer): Sub user Id
            frozen (integer): 0: unfreeze, 1: freeze

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/user/froze-subuid
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{User.FREEZE_SUB_UID}",
            query=kwargs,
            auth=True,
        )

    def get_api_key_information(self, **kwargs):
        """Get the information of the api key. Use the api key pending to be checked to call the endpoint. Both master and sub user's api key are applicable.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/user/apikey-info
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{User.GET_API_KEY_INFORMATION}",
            query=kwargs,
            auth=True,
        )

    def modify_master_api_key(self, **kwargs):
        """Modify the settings of master api key. Use the api key pending to be modified to call the endpoint. Use master user's api key only.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/user/modify-master-apikey
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{User.MODIFY_MASTER_API_KEY}",
            query=kwargs,
            auth=True,
        )

    def modify_sub_api_key(self, **kwargs):
        """Modify the settings of sub api key. Use the api key pending to be modified to call the endpoint. Use sub user's api key only.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/user/modify-sub-apikey
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{User.MODIFY_SUB_API_KEY}",
            query=kwargs,
            auth=True,
        )

    def delete_master_api_key(self, **kwargs):
        """Delete the api key of master account. Use the api key pending to be delete to call the endpoint. Use master user's api key only.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/user/rm-master-apikey
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{User.DELETE_MASTER_API_KEY}",
            query=kwargs,
            auth=True,
        )

    def delete_sub_api_key(self, **kwargs):
        """Delete the api key of sub account. Use the api key pending to be delete to call the endpoint. Use sub user's api key only.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/user/rm-sub-apikey
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{User.DELETE_SUB_API_KEY}",
            query=kwargs,
            auth=True,
        )

    def delete_sub_uid(self, **kwargs):
        """Delete a sub UID. Before deleting the sub UID, please make sure there is no asset. Use master user's api key only.

        Required args:
            subMemberId (integer): Sub UID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/user/rm-subuid
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{User.DELETE_SUB_UID}",
            query=kwargs,
            auth=True,
        )

    def get_all_sub_api_keys(self, **kwargs):
        """Query all api keys information of a sub UID.

        Required args:
            subMemberId (integer): Sub UID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/user/list-sub-apikeys
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{User.GET_ALL_SUB_API_KEYS}",
            query=kwargs,
            auth=True,
        )

    def get_affiliate_user_info(self, **kwargs):
        """This API is used for affiliate to get their users information

        Required args:
            uid (integer): The master account uid of affiliate's client

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/user/affiliate-info
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{User.GET_AFFILIATE_USER_INFO}",
            query=kwargs,
            auth=True,
        )

    def get_uid_wallet_type(self, **kwargs):
        """Get available wallet types for the master account or sub account

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/user/wallet-type
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{User.GET_UID_WALLET_TYPE}",
            query=kwargs,
            auth=True,
        )
