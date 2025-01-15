from dataclasses import dataclass
from ._v5_misc import MiscASYNCHTTP
from ._v5_market import MarketASYNCHTTP
from ._v5_trade import TradeASYNCHTTP
from ._v5_account import AccountASYNCHTTP
from ._v5_asset import AssetASYNCHTTP
from ._v5_position import PositionASYNCHTTP
from ._v5_pre_upgrade import PreUpgradeASYNCHTTP
from ._v5_spot_leverage_token import SpotLeverageASYNCHTTP
from ._v5_spot_margin_trade import SpotMarginTradeASYNCHTTP
from ._v5_user import UserASYNCHTTP
from ._v5_broker import BrokerASYNCHTTP
from ._v5_institutional_loan import InstitutionalLoanASYNCHTTP


WSS_NAME = "Unified V5"
PRIVATE_WSS = "wss://{SUBDOMAIN}.{DOMAIN}.com/v5/private"
PUBLIC_WSS = "wss://{SUBDOMAIN}.{DOMAIN}.com/v5/public/{CHANNEL_TYPE}"
AVAILABLE_CHANNEL_TYPES = [
    "inverse",
    "linear",
    "spot",
    "option",
    "private",
]

@dataclass
class HTTP(
    MiscASYNCHTTP,
    MarketASYNCHTTP,
    TradeASYNCHTTP,
    AccountASYNCHTTP,
    AssetASYNCHTTP,
    PositionASYNCHTTP,
    PreUpgradeASYNCHTTP,
    SpotLeverageASYNCHTTP,
    SpotMarginTradeASYNCHTTP,
    UserASYNCHTTP,
    BrokerASYNCHTTP,
    InstitutionalLoanASYNCHTTP,
):
    def __init__(self, **args):
        super().__init__(**args)