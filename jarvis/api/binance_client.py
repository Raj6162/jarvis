import requests

BASE_URL = "https://fapi.binance.com"

# ---------------- OHLC ---------------- #

def fetch_klines(symbol, interval="5m", limit=20):

    url = f"{BASE_URL}/fapi/v1/klines"

    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }

    response = requests.get(url, params=params)

    data = response.json()

    candles = []

    for c in data:
        candles.append({
            "open": float(c[1]),
            "high": float(c[2]),
            "low": float(c[3]),
            "close": float(c[4]),
            "volume": float(c[5])
        })

    return candles

# ---------------- OPEN INTEREST ---------------- #

def fetch_open_interest(symbol, period="5m", limit=10):

    url = f"{BASE_URL}/futures/data/openInterestHist"

    params = {
        "symbol": symbol,
        "period": period,
        "limit": limit
    }

    response = requests.get(url, params=params)

    return response.json()

# ---------------- FUNDING RATE ---------------- #

def fetch_funding_rate(symbol, limit=5):

    url = f"{BASE_URL}/fapi/v1/fundingRate"

    params = {
        "symbol": symbol,
        "limit": limit
    }

    response = requests.get(url, params=params)

    return response.json()

# ---------------- LONG SHORT RATIO ---------------- #

def fetch_long_short_ratio(symbol, period="5m", limit=10):

    url = f"{BASE_URL}/futures/data/globalLongShortAccountRatio"

    params = {
        "symbol": symbol,
        "period": period,
        "limit": limit
    }

    response = requests.get(url, params=params)

    return response.json()