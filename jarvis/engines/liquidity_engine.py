def detect_liquidity_sweep(candles):

    if len(candles) < 3:
        return "No sweep detected"

    prev = candles[-2]
    current = candles[-1]

    prev_high = prev[1]
    prev_low = prev[2]

    current_high = current[1]
    current_low = current[2]
    current_close = current[3]

    # ---------- Bearish Sweep ---------- #

    if current_high > prev_high and current_close < prev_high:
        return "Bearish liquidity sweep detected"

    # ---------- Bullish Sweep ---------- #

    if current_low < prev_low and current_close > prev_low:
        return "Bullish liquidity sweep detected"

    return "No liquidity sweep detected"
def detect_fvg(candles):

    if len(candles) < 3:
        return "No FVG detected"

    c1 = candles[-3]
    c2 = candles[-2]
    c3 = candles[-1]

    # OHLCV format
    c1_high = c1[1]
    c1_low = c1[2]

    c3_high = c3[1]
    c3_low = c3[2]

    # ---------- Bullish FVG ---------- #

    if c3_low > c1_high:
        return "Bullish FVG detected"

    # ---------- Bearish FVG ---------- #

    if c3_high < c1_low:
        return "Bearish FVG detected"

    return "No FVG detected"