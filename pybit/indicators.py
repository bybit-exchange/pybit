# pybit/indicators.py
from typing import Any, Callable, List, Sequence


class Indicators:
    """
    Small helper class for technical indicators using a pybit HTTP client.
    The http_client must expose a method that returns kline/candlestick data.
    Common names: `get_kline`, `kline`, `get_candles` — adapt the call in `_fetch_klines`
    if your local pybit client uses a different method name.
    """

    def __init__(self, http_client: Any, kline_fetcher: str | None = None):
        """
        :param http_client: pybit HTTP client instance (or any object exposing a kline fetcher)
        :param kline_fetcher: optional method name on http_client to call for klines.
                              If None, we try some common method names.
        """
        self._http = http_client
        self._kline_fetcher = kline_fetcher

    def _fetch_klines(self, symbol: str, interval: str, limit: int) -> Any:
        """
        Call the client's kline method. Tries the provided kline_fetcher name,
        else tries common names.
        """
        method_names = [self._kline_fetcher] if self._kline_fetcher else []
        method_names += ["get_kline", "kline", "get_klines", "get_candles", "kline_data"]

        for name in method_names:
            if not name:
                continue
            fetcher = getattr(self._http, name, None)
            if callable(fetcher):
                # attempt call — adapt param names if necessary
                try:
                    return fetcher(symbol=symbol, interval=interval, limit=limit)
                except TypeError:
                    # maybe client uses different parameter names (like interval=60)
                    try:
                        return fetcher(symbol=symbol, kline_type=interval, limit=limit)
                    except Exception:
                        # fallback — let the next fetcher try
                        continue

        # If no fetcher found, raise so caller adapts to their client
        raise RuntimeError(
            "Could not find a kline fetch method on http client. "
            "Pass `kline_fetcher` with the method name or adapt Indicators._fetch_klines."
        )

    @staticmethod
    def _normalize_klines(raw: Any) -> List[Sequence]:
        """
        Normalizes possible shapes of kline responses into a list of sequences.
        Supports common shapes:
          - list of lists: [[open_time, open, high, low, close, ...], ...]
          - dict with 'result' containing 'list' (some APIs)
          - dict with 'data' or 'result' that is a list of dicts: [{'close': '123.4'}, ...]
        """
        # raw could be the list directly
        if isinstance(raw, list):
            return raw

        if isinstance(raw, dict):
            # common wrappers
            for key in ("result", "data", "response"):
                if key in raw:
                    inner = raw[key]
                    if isinstance(inner, list):
                        return inner
                    if isinstance(inner, dict):
                        # maybe inner contains a 'list' key
                        if "list" in inner and isinstance(inner["list"], list):
                            return inner["list"]
            # fallback: if it looks like dict-of-lists
            for v in raw.values():
                if isinstance(v, list):
                    return v

        raise ValueError("Unrecognized kline response format")

    @staticmethod
    def _extract_closes(klines: List[Sequence]) -> List[float]:
        """
        Extract close prices from kline rows.
        Supports:
          - list rows where index 4 is close
          - dict rows with 'close', 'Close', or 'close_price' keys
        """
        closes: List[float] = []
        for row in klines:
            if isinstance(row, (list, tuple)):
                # common format: [open_time, open, high, low, close, volume, ...]
                try:
                    close_val = float(row[4])
                except Exception as e:
                    raise ValueError(f"Cannot parse close from row {row}: {e}")
            elif isinstance(row, dict):
                # try common key names
                for key in ("close", "Close", "closePrice", "close_price", "c"):
                    if key in row:
                        close_val = float(row[key])
                        break
                else:
                    raise ValueError(f"No close field found in kline dict: {row}")
            else:
                raise ValueError(f"Unsupported kline row type: {type(row)}")
            closes.append(close_val)
        return closes

    def get_momentum(self, symbol: str, interval: str = "60", lookback: int = 14) -> float:
        """
        Calculate Momentum = Close[t] - Close[t-lookback]
        :param symbol: trading symbol (e.g. "BTCUSDT")
        :param interval: interval string/identifier (depends on client; "60" for 1h)
        :param lookback: lookback period (integer)
        :returns: momentum as a float
        """
        if lookback < 1:
            raise ValueError("lookback must be >= 1")

        raw = self._fetch_klines(symbol=symbol, interval=interval, limit=lookback + 1)
        klines = self._normalize_klines(raw)
        if len(klines) < lookback + 1:
            raise ValueError(f"Not enough klines returned: needed {lookback+1}, got {len(klines)}")

        # klines may be newest-first or oldest-first depending on client. We attempt to detect:
        # if the first timestamp > last timestamp (descending), reverse to ascending.
        # For list-of-lists where index 0 is timestamp:
        try:
            first_ts = float(klines[0][0])
            last_ts = float(klines[-1][0])
            if first_ts > last_ts:
                klines = list(reversed(klines))
        except Exception:
            # If we can't determine, assume returned klines are oldest->newest
            pass

        closes = self._extract_closes(klines)
        momentum = closes[-1] - closes[0]  # most recent close minus the close lookback periods ago
        return momentum
