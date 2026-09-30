from unittest.mock import Mock

import pytest

from pybit.unified_trading import HTTP
from pybit._v5_crypto_loan import CryptoLoanHTTP
from pybit.crypto_loan import CryptoLoan
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
}


@pytest.mark.parametrize("name,url", DOC_URLS.items(), ids=DOC_URLS)
def test_generated_method_links_to_matching_documentation(name, url):
    assert url in getattr(HTTP, name).__doc__
