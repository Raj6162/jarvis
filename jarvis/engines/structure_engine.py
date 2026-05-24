def detect_swings(candles):

    swing_highs = []
    swing_lows = []

    for i in range(1, len(candles) - 1):

        prev_candle = candles[i - 1]
        current = candles[i]
        next_candle = candles[i + 1]

        current_high = current[1]
        current_low = current[2]

        # ---------- Swing High ---------- #

        if (
            current_high > prev_candle[1]
            and current_high > next_candle[1]
        ):

            swing_highs.append(current_high)

        # ---------- Swing Low ---------- #

        if (
            current_low < prev_candle[2]
            and current_low < next_candle[2]
        ):

            swing_lows.append(current_low)

    return swing_highs, swing_lows


def detect_structure(candles):

    if len(candles) < 10:
        return {
            "trend": "Unknown",
            "bos": "No BOS",
            "choch": "No CHOCH"
        }

    swing_highs, swing_lows = detect_swings(candles)

    if len(swing_highs) < 2 or len(swing_lows) < 2:
        return {
            "trend": "Ranging",
            "bos": "No BOS",
            "choch": "No CHOCH"
        }

    last_high = swing_highs[-1]
    prev_high = swing_highs[-2]

    last_low = swing_lows[-1]
    prev_low = swing_lows[-2]

    trend = "Ranging"
    bos = "No BOS"
    choch = "No CHOCH"

    # ---------- Bullish Structure ---------- #

    if last_high > prev_high and last_low > prev_low:

        trend = "Bullish"
        bos = "Bullish BOS detected"

    # ---------- Bearish Structure ---------- #

    elif last_high < prev_high and last_low < prev_low:

        trend = "Bearish"
        bos = "Bearish BOS detected"

    # ---------- CHOCH ---------- #

    elif last_high > prev_high and last_low < prev_low:

        choch = "Volatile CHOCH / possible reversal"

    return {
        "trend": trend,
        "bos": bos,
        "choch": choch
    }