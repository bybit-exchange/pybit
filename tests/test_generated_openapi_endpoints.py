from unittest.mock import Mock

import pytest

from pybit.unified_trading import HTTP


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
    ("create_chase_order_strategy", "POST", "/v5/strategy/create"),
    ("query_strategy_list", "GET", "/v5/strategy/list"),
    ("query_strategy_order_list", "GET", "/v5/strategy/order-list"),
    ("stop_strategy", "POST", "/v5/strategy/stop"),
]


@pytest.mark.parametrize("name,method,path", CASES, ids=[case[0] for case in CASES])
def test_generated_endpoint_dispatch(name, method, path):
    client = HTTP.__new__(HTTP)
    client.endpoint = "https://api.bybit.com"
    client._submit_request = Mock(side_effect=lambda **kwargs: kwargs)

    result = getattr(client, name)(probe="value")

    assert result == {
        "method": method,
        "path": f"https://api.bybit.com{path}",
        "query": {"probe": "value"},
        "auth": True,
    }
