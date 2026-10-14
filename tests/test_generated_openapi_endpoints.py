from pathlib import Path
from unittest.mock import Mock

import pytest

from pybit.unified_trading import HTTP
from pybit.asset import Asset
from pybit._v5_crypto_loan import CryptoLoanHTTP
from pybit.crypto_loan import CryptoLoan
from pybit.institutional_loan import InstitutionalLoan
from pybit.strategy import Strategy


CASES = [
    ("get_crypto_loan_fixed_available_inventory", "GET", "/v5/crypto-loan-fixed/available-inventory"),
    ("get_crypto_loan_flexible_available_inventory", "GET", "/v5/crypto-loan-flexible/available-inventory"),
    ("close_dca_bot", "POST", "/v5/dca/close-bot"),
    ("create_dca_bot", "POST", "/v5/dca/create-bot"),
    ("close_combo_bot", "POST", "/v5/fcombobot/close"),
    ("create_combo_bot", "POST", "/v5/fcombobot/create"),
    ("get_combo_detail", "POST", "/v5/fcombobot/detail"),
    ("get_combo_limit", "POST", "/v5/fcombobot/getlimit"),
    ("close_f_grid_bot", "POST", "/v5/fgridbot/close"),
    ("create_f_grid_bot", "POST", "/v5/fgridbot/create"),
    ("get_f_grid_detail", "POST", "/v5/fgridbot/detail"),
    ("validate_f_grid_input", "POST", "/v5/fgridbot/validate"),
    ("batch_create_tax_reports", "POST", "/v5/fht/compliance/tax/private/batch_create"),
    ("batch_query_tax_reports", "GET", "/v5/fht/compliance/tax/private/batch_query"),
    ("close_f_mart_bot", "POST", "/v5/fmartingalebot/close"),
    ("create_f_mart_bot", "POST", "/v5/fmartingalebot/create"),
    ("get_f_mart_detail", "POST", "/v5/fmartingalebot/detail"),
    ("get_f_mart_limit", "POST", "/v5/fmartingalebot/getlimit"),
    ("close_grid_bot", "POST", "/v5/grid/close-grid"),
    ("create_grid_bot", "POST", "/v5/grid/create-grid"),
    ("query_grid_detail", "POST", "/v5/grid/query-grid-detail"),
    ("validate_grid_input", "POST", "/v5/grid/validate-input"),
    ("get_convert_detail", "GET", "/v5/rwa/stocks/convert/detail"),
    ("get_convert_list", "GET", "/v5/rwa/stocks/convert/list"),
    ("submit_convert", "POST", "/v5/rwa/stocks/convert/submit"),
    ("get_multiplier_list", "GET", "/v5/rwa/stocks/market/getMultiplierList"),
    ("get_market_session", "GET", "/v5/rwa/stocks/market/session"),
    ("place_stocks_order", "POST", "/v5/rwa/stocks/order"),
    ("cancel_stocks_order", "POST", "/v5/rwa/stocks/order/cancel"),
    ("get_stocks_order_detail", "GET", "/v5/rwa/stocks/order/detail"),
    ("get_stocks_positions", "GET", "/v5/rwa/stocks/positions"),
    ("create_strategy", "POST", "/v5/strategy/create", True),
    ("create_chase_order_strategy", "POST", "/v5/strategy/create", True),
    ("create_twap_strategy", "POST", "/v5/strategy/create", True),
    ("create_iceberg_strategy", "POST", "/v5/strategy/create", True),
    ("create_pov_strategy", "POST", "/v5/strategy/create", True),
    ("query_strategy_list", "GET", "/v5/strategy/list", True),
    ("query_strategy_order_list", "GET", "/v5/strategy/order-list", True),
    ("stop_strategy", "POST", "/v5/strategy/stop", True),
    ("get_option_base_coins", "GET", "/v5/market/option-base-coins", None),
    ("get_option_asset_info", "GET", "/v5/account/option-asset-info"),
    ("get_pay_info", "GET", "/v5/account/pay-info"),
    ("get_trade_info_for_analysis", "GET", "/v5/account/trade-info-for-analysis"),
    ("get_portfolio_margin", "GET", "/v5/asset/portfolio-margin"),
    ("get_total_members_assets", "GET", "/v5/asset/total-members-assets"),
    ("list_earn_auto_savings", "GET", "/v5/earn/flexible-saving/auto-savings"),
    ("edit_earn_auto_savings", "POST", "/v5/earn/flexible-saving/auto-savings"),
    ("ins_loan_coin_delta_amount", "GET", "/v5/ins-loan/coin-delta-amount"),
    ("ins_loan_delay_liq_status", "GET", "/v5/ins-loan/delay-liq-status"),
    ("get_position_symbol_info", "GET", "/v5/position/symbol-info"),
    ("query_fixed_available_inventory", "GET", "/v5/spot-margin-trade/fixed-available-inventory"),
    ("account_fixed_borrow", "POST", "/v5/spot-margin-trade/fixedborrow"),
    ("query_fixed_borrow_contracts", "GET", "/v5/spot-margin-trade/fixedborrow-contract-info"),
    ("query_fixed_borrow_orders", "GET", "/v5/spot-margin-trade/fixedborrow-order-info"),
    ("query_fixed_borrow_market", "GET", "/v5/spot-margin-trade/fixedborrow-order-quote"),
    ("renew_fixed_borrow", "POST", "/v5/spot-margin-trade/fixedborrow-renew"),
    ("get_spot_margin_trade_flexible_available_inventory", "GET", "/v5/spot-margin-trade/flexible-available-inventory"),
    ("query_borrow_liability", "GET", "/v5/spot-margin-trade/liability"),
    ("get_spread_max_qty", "GET", "/v5/spread/max-qty"),
    ("query_referral_code", "GET", "/v5/user/invitation/code"),
]


STRATEGY_TYPES = {
    "create_chase_order_strategy": "chaseOrder",
    "create_twap_strategy": "twap",
    "create_iceberg_strategy": "iceberg",
    "create_pov_strategy": "pov",
}


CASES = [
    (*case, True) if len(case) == 3 else case
    for case in CASES
]


@pytest.mark.parametrize("name,method,path,auth", CASES, ids=[case[0] for case in CASES])
def test_generated_endpoint_dispatch(name, method, path, auth):
    client = HTTP.__new__(HTTP)
    client.endpoint = "https://api.bybit.com"
    client._submit_request = Mock(side_effect=lambda **kwargs: kwargs)

    result = getattr(client, name)(probe="value")

    expected = {
        "method": method,
        "path": f"https://api.bybit.com{path}",
        "query": {"probe": "value"},
    }
    if name in STRATEGY_TYPES:
        expected["query"]["strategyType"] = STRATEGY_TYPES[name]
    if auth is not None:
        expected["auth"] = auth

    assert result == expected


def test_crypto_loan_inventory_endpoints_use_existing_service_modules():
    assert hasattr(CryptoLoanHTTP, "get_crypto_loan_fixed_available_inventory")
    assert hasattr(CryptoLoanHTTP, "get_crypto_loan_flexible_available_inventory")
    assert CryptoLoan.GET_CRYPTO_LOAN_FIXED_AVAILABLE_INVENTORY == (
        "/v5/crypto-loan-fixed/available-inventory"
    )
    assert CryptoLoan.GET_CRYPTO_LOAN_FLEXIBLE_AVAILABLE_INVENTORY == (
        "/v5/crypto-loan-flexible/available-inventory"
    )


@pytest.mark.parametrize(
    "name,strategy_type",
    STRATEGY_TYPES.items(),
)
def test_strategy_alias_supplies_strategy_type(name, strategy_type):
    client = HTTP.__new__(HTTP)
    client.endpoint = "https://api.bybit.com"
    client._submit_request = Mock(side_effect=lambda **kwargs: kwargs)

    result = getattr(client, name)(symbol="BTCUSDT")

    assert result["query"]["strategyType"] == strategy_type


@pytest.mark.parametrize(
    "name,strategy_type",
    STRATEGY_TYPES.items(),
)
def test_strategy_alias_rejects_conflicting_strategy_type(name, strategy_type):
    client = HTTP.__new__(HTTP)
    client.endpoint = "https://api.bybit.com"
    client._submit_request = Mock(side_effect=lambda **kwargs: kwargs)

    with pytest.raises(ValueError, match=f"requires strategyType={strategy_type}"):
        getattr(client, name)(strategyType="conflicting-type")

    client._submit_request.assert_not_called()


def test_chase_strategy_enum_key_remains_canonical_for_compatibility():
    assert Strategy.CREATE_CHASE_ORDER_STRATEGY.name == (
        "CREATE_CHASE_ORDER_STRATEGY"
    )
    assert Strategy.CREATE_STRATEGY is Strategy.CREATE_CHASE_ORDER_STRATEGY


@pytest.mark.parametrize("name", ["create_grid_bot", "validate_grid_input"])
def test_spot_grid_docs_use_current_investment_parameters(name):
    doc = getattr(HTTP, name).__doc__

    assert "total_investment" not in doc
    assert "invest_mode" in doc
    assert "base_investment" in doc
    assert "quote_investment" in doc
    assert doc.count("Required when invest_mode") == 2


DOC_URLS = {
    "close_dca_bot": "/docs/v5/bot/dca/close",
    "create_dca_bot": "/docs/v5/bot/dca/create",
    "close_combo_bot": "/docs/v5/bot/futures-combo/close",
    "create_combo_bot": "/docs/v5/bot/futures-combo/create",
    "get_combo_detail": "/docs/v5/bot/futures-combo/get-detail",
    "get_combo_limit": "/docs/v5/bot/futures-combo/get-limit",
    "close_f_grid_bot": "/docs/v5/bot/futures-grid/close",
    "create_f_grid_bot": "/docs/v5/bot/futures-grid/create",
    "get_f_grid_detail": "/docs/v5/bot/futures-grid/get-detail",
    "validate_f_grid_input": "/docs/v5/bot/futures-grid/validate-input",
    "close_f_mart_bot": "/docs/v5/bot/futures-martingale/close",
    "create_f_mart_bot": "/docs/v5/bot/futures-martingale/create",
    "get_f_mart_detail": "/docs/v5/bot/futures-martingale/get-detail",
    "get_f_mart_limit": "/docs/v5/bot/futures-martingale/get-limit",
    "close_grid_bot": "/docs/v5/bot/spot-grid/close",
    "create_grid_bot": "/docs/v5/bot/spot-grid/create",
    "query_grid_detail": "/docs/v5/bot/spot-grid/get-detail",
    "validate_grid_input": "/docs/v5/bot/spot-grid/validate-input",
    "create_strategy": "/docs/v5/strategy/create-strategy",
    "query_strategy_list": "/docs/v5/strategy/strategy-list",
    "query_strategy_order_list": "/docs/v5/strategy/order-list",
    "stop_strategy": "/docs/v5/strategy/stop-strategy",
    "get_option_asset_info": "/docs/v5/account/option-asset-info",
    "get_pay_info": "/docs/v5/account/pay-info",
    "get_trade_info_for_analysis": "/docs/v5/account/trade-info-for-analysis",
    "get_portfolio_margin": "/docs/v5/asset/portfolio-margin",
    "get_total_members_assets": "/docs/v5/asset/total-members-assets",
    "list_earn_auto_savings": "/docs/v5/finance/earn/flexible-saving/auto-savings",
    "edit_earn_auto_savings": "/docs/v5/finance/earn/flexible-saving/auto-savings",
    "ins_loan_coin_delta_amount": "/docs/v5/otc/coin-delta-amount",
    "ins_loan_delay_liq_status": "/docs/v5/otc/delay-liq-status",
    "get_position_symbol_info": "/docs/v5/position/batch-lvg",
    "query_fixed_available_inventory": "/docs/v5/spot-margin-uta/fixed-available-inventory",
    "account_fixed_borrow": "/docs/v5/spot-margin-uta/fixedborrow",
    "query_fixed_borrow_contracts": "/docs/v5/spot-margin-uta/fixedborrow-contract-info",
    "query_fixed_borrow_orders": "/docs/v5/spot-margin-uta/fixedborrow-order-info",
    "query_fixed_borrow_market": "/docs/v5/spot-margin-uta/fixedborrow-order-quote",
    "renew_fixed_borrow": "/docs/v5/spot-margin-uta/fixedborrow-renew",
    "get_spot_margin_trade_flexible_available_inventory": "/docs/v5/spot-margin-uta/flexible-available-inventory",
    "query_borrow_liability": "/docs/v5/spot-margin-uta/liability",
    "get_spread_max_qty": "/docs/v5/spread/trade/max-qty",
    "query_referral_code": "/docs/v5/user/referral-code",
}


@pytest.mark.parametrize("name,url", DOC_URLS.items(), ids=DOC_URLS)
def test_generated_method_links_to_matching_documentation(name, url):
    assert url in getattr(HTTP, name).__doc__


REMOVED_METHODS = [
    "query_sub_member_deposit_records",
    "inter_transfer_list_query",
    "universal_transfer_list_query",
    "ins_loan_association_uid",
    "ins_loan_ensure_tokens",
    "ins_loan_ensure_tokens_convert",
    "ins_loan_get_loan_order",
    "ins_loan_ltv_convert",
    "ins_loan_product_infos",
    "ins_loan_repaid_history",
    "ins_loan_repay_loan",
]


@pytest.mark.parametrize("name", REMOVED_METHODS)
def test_release_does_not_expose_duplicate_or_abandoned_methods(name):
    assert not hasattr(HTTP, name)


def test_release_does_not_expose_duplicate_or_abandoned_endpoint_keys():
    asset_keys = {
        "QUERY_SUB_MEMBER_DEPOSIT_RECORDS",
        "INTER_TRANSFER_LIST_QUERY",
        "UNIVERSAL_TRANSFER_LIST_QUERY",
    }
    institutional_loan_keys = {
        "INS_LOAN_ASSOCIATION_UID",
        "INS_LOAN_ENSURE_TOKENS",
        "INS_LOAN_ENSURE_TOKENS_CONVERT",
        "INS_LOAN_GET_LOAN_ORDER",
        "INS_LOAN_LTV_CONVERT",
        "INS_LOAN_PRODUCT_INFOS",
        "INS_LOAN_REPAID_HISTORY",
        "INS_LOAN_REPAY_LOAN",
    }

    assert asset_keys.isdisjoint(Asset.__members__)
    assert institutional_loan_keys.isdisjoint(InstitutionalLoan.__members__)


def test_fixed_borrow_market_docs_mark_order_by_optional():
    doc = HTTP.query_fixed_borrow_market.__doc__

    assert "Optional args:" in doc
    required, optional = doc.split("Optional args:", 1)
    assert "orderBy" not in required
    assert "orderBy" in optional


def test_spread_max_qty_docs_use_endpoint_title():
    assert HTTP.get_spread_max_qty.__doc__.strip().splitlines()[0] == (
        "Get Spread Max Qty"
    )


def test_changelog_lists_only_supported_5_17_2_methods():
    changelog = Path("CHANGELOG.md").read_text()
    section = changelog.split("## [5.17.2] - 2026-10-13", 1)[1]
    methods = section.split("### New Methods (20)", 1)[1]
    methods = methods.split("### New Endpoint Keys", 1)[0]
    listed_methods = {
        line.removeprefix("- `").removesuffix("`")
        for line in methods.splitlines()
        if line.startswith("- `")
    }
    expected_methods = {case[0] for case in CASES[-20:]}

    assert listed_methods == expected_methods
