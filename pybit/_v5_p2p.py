from ._http_manager import _V5HTTPManager
from .p2p import P2P


class P2PHTTP(_V5HTTPManager):
    def get_current_balance(self, **kwargs):
        """Get current funding account balance for P2P.

        Required args:
            accountType (string): Account type

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/p2p/all-balance
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{P2P.GET_CURRENT_BALANCE}",
            query=kwargs,
            auth=True,
        )

    def get_account_information(self, **kwargs):
        """Get P2P account information.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/p2p/user/acct-info
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{P2P.GET_ACCOUNT_INFORMATION}",
            query=kwargs,
            auth=True,
        )

    def get_ads_list(self, **kwargs):
        """Get your P2P ads list.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/p2p/ad/ad-list
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{P2P.GET_ADS_LIST}",
            query=kwargs,
            auth=True,
        )

    def get_ad_details(self, **kwargs):
        """Get your P2P ad details.

        Required args:
            itemId (string): Advertisement ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/p2p/ad/ad-detail
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{P2P.GET_AD_DETAILS}",
            query=kwargs,
            auth=True,
        )

    def update_ad(self, **kwargs):
        """Update or relist a P2P ad.

        Required args:
            id (string): Advertisement ID
            priceType (string): Price type
            premium (string): Floating ratio
            price (string): Advertisement price
            minAmount (string): Minimum transaction amount
            maxAmount (string): Maximum transaction amount
            remark (string): Advertisement description
            tradingPreferenceSet (object): Trading preferences
            paymentIds (array): Payment method IDs
            actionType (string): MODIFY or ACTIVE
            quantity (string): Quantity
            paymentPeriod (string): Payment duration

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/p2p/ad/update-list-ad
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{P2P.UPDATE_AD}",
            query=kwargs,
            auth=True,
        )

    def remove_ad(self, **kwargs):
        """Remove a P2P ad.

        Required args:
            itemId (string): Advertisement ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/p2p/ad/remove-ad
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{P2P.REMOVE_AD}",
            query=kwargs,
            auth=True,
        )

    def get_orders(self, **kwargs):
        """Get all P2P orders.

        Required args:
            page (string): Page number
            size (string): Rows per page

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/p2p/order/order-list
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{P2P.GET_ORDERS}",
            query=kwargs,
            auth=True,
        )

    def get_pending_orders(self, **kwargs):
        """Get pending P2P orders.

        Required args:
            page (string): Page number
            size (string): Rows per page

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/p2p/order/pending-order
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{P2P.GET_PENDING_ORDERS}",
            query=kwargs,
            auth=True,
        )

    def get_counterparty_info(self, **kwargs):
        """Get counterparty user information.

        Required args:
            originalUid (string): Counterparty UID
            orderId (string): Order ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/p2p/user/counterparty-user-info
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{P2P.GET_COUNTERPARTY_INFO}",
            query=kwargs,
            auth=True,
        )

    def get_order_details(self, **kwargs):
        """Get P2P order details.

        Required args:
            orderId (string): Order ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/p2p/order/order-detail
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{P2P.GET_ORDER_DETAILS}",
            query=kwargs,
            auth=True,
        )

    def release_assets(self, **kwargs):
        """Release digital assets to the buyer.

        Required args:
            orderId (string): Order ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/p2p/order/release-digital-asset
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{P2P.RELEASE_ASSETS}",
            query=kwargs,
            auth=True,
        )

    def mark_as_paid(self, **kwargs):
        """Mark a P2P order as paid.

        Required args:
            orderId (string): Order ID
            paymentType (string): Payment method type
            paymentId (string): Payment method ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/p2p/order/mark-order-as-paid
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{P2P.MARK_AS_PAID}",
            query=kwargs,
            auth=True,
        )

    def get_chat_messages(self, **kwargs):
        """Get P2P order chat messages.

        Required args:
            orderId (string): Order ID
            size (string): Page size

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/p2p/order/chat-msg
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{P2P.GET_CHAT_MESSAGES}",
            query=kwargs,
            auth=True,
        )

    def upload_chat_file(self, **kwargs):
        """Upload a file for P2P chat.

        Required args:
            upload_file (string, bytes, or file-like): File to upload

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/p2p/order/upload-chat-file
        """
        return self._submit_file_request(
            path=f"{self.endpoint}{P2P.UPLOAD_CHAT_FILE}",
            query=kwargs,
            auth=True,
        )

    def send_chat_message(self, **kwargs):
        """Send a P2P order chat message.

        Required args:
            message (string): Chat message
            contentType (string): Chat message type
            orderId (string): Order ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/p2p/order/send-chat-msg
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{P2P.SEND_CHAT_MESSAGE}",
            query=kwargs,
            auth=True,
        )

    def post_new_ad(self, **kwargs):
        """Post a new P2P ad.

        Required args:
            tokenId (string): Token ID
            currencyId (string): Currency ID
            side (string): Buy or sell side
            priceType (string): Price type
            premium (string): Floating ratio
            price (string): Advertisement price
            minAmount (string): Minimum transaction amount
            maxAmount (string): Maximum transaction amount
            remark (string): Advertisement description
            tradingPreferenceSet (object): Trading preferences
            paymentIds (array): Payment method IDs
            quantity (string): Quantity
            paymentPeriod (string): Payment duration
            itemType (string): Advertisement type

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/p2p/ad/post-new-ad
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{P2P.POST_NEW_AD}",
            query=kwargs,
            auth=True,
        )

    def get_online_ads(self, **kwargs):
        """Get online P2P ads.

        Required args:
            tokenId (string): Token ID
            currencyId (string): Currency ID
            side (string): Buy or sell side

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/p2p/ad/online-ad-list
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{P2P.GET_ONLINE_ADS}",
            query=kwargs,
            auth=True,
        )

    def get_user_payment_types(self, **kwargs):
        """Get user payment methods.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/p2p/user/user-payment
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{P2P.GET_USER_PAYMENT_TYPES}",
            query=kwargs,
            auth=True,
        )

    def query_chat_session_list(self, **kwargs):
        """Query P2P chat session list.

        Required args:
            size (string): Page size

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/p2p/chat/session-list
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{P2P.QUERY_CHAT_SESSION_LIST}",
            query=kwargs,
            auth=True,
        )

    def send_message(self, **kwargs):
        """Send a P2P chat message.

        This endpoint is not recommended for general use yet.

        Required args:
            message (string): Chat message
            contentType (string): Chat message type
            sessionId (string): Encrypted session ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/p2p/chat/send-message
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{P2P.SEND_MESSAGE}",
            query=kwargs,
            auth=True,
        )

    def get_message_list(self, **kwargs):
        """Get P2P chat message list.

        This endpoint is not recommended for general use yet.

        Required args:
            limit (string): Page size
            sessionId (string): Encrypted session ID

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/p2p/chat/message-list
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{P2P.GET_MESSAGE_LIST}",
            query=kwargs,
            auth=True,
        )
