from ._http_manager import _V5HTTPManager
from .account import Account


class AccountHTTP(_V5HTTPManager):
    def get_wallet_balance(self, **kwargs):
        """Obtain wallet balance, query asset information of each currency, and account risk rate information under unified margin mode.
        By default, currency information with assets or liabilities of 0 is not returned.

        Required args:
            accountType (string): Account type
                Unified account: UNIFIED
                Normal account: CONTRACT

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/account/wallet-balance
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Account.GET_WALLET_BALANCE}",
            query=kwargs,
            auth=True,
        )

    def get_coin_withdrawal(self, **kwargs):
        """Query the available amount to transfer of a specific coin in the Unified wallet.

        Required args:
            coinName (string): Coin name, uppercase only

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/account/unified-trans-amnt
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Account.GET_COIN_WITHDRAWAL}",
            query=kwargs,
            auth=True,
        )
  
    def get_transferable_amount(self, **kwargs):
        """Query the available amount to transfer of a specific coin in the Unified wallet.

        Required args:
            coinName (string): Coin name, uppercase only

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/account/unified-trans-amnt
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Account.GET_TRANSFERABLE_AMOUNT}",
            query=kwargs,
            auth=True,
        )

    def upgrade_to_unified_trading_account(self, **kwargs):
        """Upgrade Unified Account

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/account/upgrade-unified-account
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Account.UPGRADE_TO_UNIFIED_ACCOUNT}",
            query=kwargs,
            auth=True,
        )

    def borrow(self, **kwargs):
        """
        https://bybit-exchange.github.io/docs/zh-TW/v5/account/borrow
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Account.BORROW}",
            query=kwargs,
            auth=True,
        )

    def repay(self, **kwargs):
        """
        https://bybit-exchange.github.io/docs/zh-TW/v5/account/repay
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Account.REPAY}",
            query=kwargs,
            auth=True,
        )

    def no_convert_repay(self, **kwargs):
        """
        https://bybit-exchange.github.io/docs/zh-TW/v5/account/no-convert-repay
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Account.NO_CONVERT_REPAY}",
            query=kwargs,
            auth=True,
        )

    def get_borrow_history(self, **kwargs):
        """Get interest records, sorted in reverse order of creation time.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/account/borrow-history
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Account.GET_BORROW_HISTORY}",
            query=kwargs,
            auth=True,
        )

    def repay_liability(self, **kwargs):
        """You can manually repay the liabilities of the Unified account

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/account/repay-liability
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Account.REPAY_LIABILITY}",
            query=kwargs,
            auth=True,
        )

    def get_collateral_info(self, **kwargs):
        """Get the collateral information of the current unified margin account, including loan interest rate, loanable amount, collateral conversion rate, whether it can be mortgaged as margin, etc.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/account/collateral-info
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Account.GET_COLLATERAL_INFO}",
            query=kwargs,
            auth=True,
        )

    def set_collateral_coin(self, **kwargs):
        """You can decide whether the assets in the Unified account needs to be collateral coins.

        Required args:
            coin (string): Coin name
            collateralSwitch (string): ON: switch on collateral, OFF: switch off collateral

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/account/set-collateral
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Account.SET_COLLATERAL_COIN}",
            query=kwargs,
            auth=True,
        )

    def batch_set_collateral_coin(self, **kwargs):
        """You can decide whether the assets in the Unified account needs to be collateral coins.

        Required args:
            request (array): Object
            > coin (string): Coin name
            > collateralSwitch (string): ON: switch on collateral, OFF: switch off collateral

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/account/batch-set-collateral
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Account.BATCH_SET_COLLATERAL_COIN}",
            query=kwargs,
            auth=True,
        )

    def get_coin_greeks(self, **kwargs):
        """Get current account Greeks information

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/account/coin-greeks
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Account.GET_COIN_GREEKS}",
            query=kwargs,
            auth=True,
        )

    def get_fee_rates(self, **kwargs):
        """Get the trading fee rate of derivatives.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/account/fee-rate
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Account.GET_FEE_RATE}",
            query=kwargs,
            auth=True,
        )

    def get_account_info(self, **kwargs):
        """Query the margin mode configuration of the account.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/account/account-info
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Account.GET_ACCOUNT_INFO}",
            query=kwargs,
            auth=True,
        )

    def get_transaction_log(self, **kwargs):
        """Query transaction logs in Unified account.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/account/transaction-log
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Account.GET_TRANSACTION_LOG}",
            query=kwargs,
            auth=True,
        )

    def get_contract_transaction_log(self, **kwargs):
        """Query transaction logs in Classic account.

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/account/contract-transaction-log
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Account.GET_CONTRACT_TRANSACTION_LOG}",
            query=kwargs,
            auth=True,
        )

    def set_margin_mode(self, **kwargs):
        """Default is regular margin mode. This mode is valid for USDT Perp, USDC Perp and USDC Option.

        Required args:
            setMarginMode (string): REGULAR_MARGIN, PORTFOLIO_MARGIN

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/account/set-margin-mode
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Account.SET_MARGIN_MODE}",
            query=kwargs,
            auth=True,
        )

    def set_mmp(self, **kwargs):
        """
        Market Maker Protection (MMP) is an automated mechanism designed to protect market makers (MM) against liquidity risks
        and over-exposure in the market. It prevents simultaneous trade executions on quotes provided by the MM within a short time span.
        The MM can automatically pull their quotes if the number of contracts traded for an underlying asset exceeds the configured
        threshold within a certain time frame. Once MMP is triggered, any pre-existing MMP orders will be automatically canceled,
        and new orders tagged as MMP will be rejected for a specific duration — known as the frozen period — so that MM can
        reassess the market and modify the quotes.

        Required args:
            baseCoin (strin): Base coin
            window (string): Time window (ms)
            frozenPeriod (string): Frozen period (ms). "0" means the trade will remain frozen until manually reset
            qtyLimit (string): Trade qty limit (positive and up to 2 decimal places)
            deltaLimit (string): Delta limit (positive and up to 2 decimal places)

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/account/set-mmp
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Account.SET_MMP}",
            query=kwargs,
            auth=True,
        )

    def reset_mmp(self, **kwargs):
        """Once the mmp triggered, you can unfreeze the account by this endpoint

        Required args:
            baseCoin (string): Base coin

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/account/reset-mmp
        """
        return self._submit_request(
            method="POST",
            path=f"{self.endpoint}{Account.RESET_MMP}",
            query=kwargs,
            auth=True,
        )

    def get_mmp_state(self, **kwargs):
        """Get MMP state

        Required args:
            baseCoin (string): Base coin

        Returns:
            Request results as dictionary.

        Additional information:
            https://bybit-exchange.github.io/docs/v5/account/get-mmp-state
        """
        return self._submit_request(
            method="GET",
            path=f"{self.endpoint}{Account.GET_MMP_STATE}",
            query=kwargs,
            auth=True,
        )
