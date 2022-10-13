import time
import re
import copy


def generate_timestamp():
    """
    Return a millisecond integer timestamp.
    """
    return int(time.time() * 10 ** 3)


def identify_ws_method(input_wss_url, wss_dictionary):
    """
    This method matches the input_wss_url with a particular WSS method. This
    helps ensure that, when subscribing to a custom topic, the topic
    subscription message is sent down the correct WSS connection.
    """
    path = re.compile("(wss://)?([^/\s]+)(.*)")
    input_wss_url_path = path.match(input_wss_url).group(3)
    for wss_url, function_call in wss_dictionary.items():
        wss_url_path = path.match(wss_url).group(3)
        if input_wss_url_path == wss_url_path:
            return function_call


def find_index(source, target, key):
    """
    Find the index in source list of the targeted ID.
    """
    return next(i for i, j in enumerate(source) if j[key] == target[key])


def make_public_kwargs(private_kwargs):
    public_kwargs = copy.deepcopy(private_kwargs)
    public_kwargs.pop("api_key", "")
    public_kwargs.pop("api_secret", "")
    return public_kwargs

def error_link(path, number):
    if "spot" in path:
        number = -1*number
        return  f" https://bybit-exchange.github.io/docs/spot/#{number}"
    elif "account_asset" in path:  # account asset
        return f" https://bybit-exchange.github.io/docs/account_asset/#{number}",
    elif "usdc" in path:  # USDC
        if "option" in path:  # option
            return f" https://bybit-exchange.github.io/docs/usdc/option/#{number}"
        else:  # perpetual
            return f" https://bybit-exchange.github.io/docs/usdc/perpetual/#{number}"
    else:  # inverse perpetual, USDT perpetual, inverse futures
        return f" https://bybit-exchange.github.io/docs/inverse/#{number}"