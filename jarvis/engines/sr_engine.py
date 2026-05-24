def detect_sr(candles):

    if len(candles) < 20:

        return {
            "resistance_zone": "Unknown",
            "support_zone": "Unknown"
        }

    swing_highs = []
    swing_lows = []

    # ---------- DETECT SWINGS ---------- #

    for i in range(1, len(candles) - 1):

        prev_candle = candles[i - 1]
        current = candles[i]
        next_candle = candles[i + 1]

        current_high = current[1]
        current_low = current[2]

        # ---------- SWING HIGH ---------- #

        if (
            current_high > prev_candle[1]
            and current_high > next_candle[1]
        ):

            swing_highs.append(current_high)

        # ---------- SWING LOW ---------- #

        if (
            current_low < prev_candle[2]
            and current_low < next_candle[2]
        ):

            swing_lows.append(current_low)

    # ---------- RESISTANCE ZONE ---------- #

    resistance_zone = "Unknown"

    if len(swing_highs) >= 2:

        recent_highs = swing_highs[-3:]

        resistance_low = min(recent_highs)
        resistance_high = max(recent_highs)

        resistance_zone = (
            f"{round(resistance_low,2)}"
            f" - "
            f"{round(resistance_high,2)}"
        )

    # ---------- SUPPORT ZONE ---------- #

    support_zone = "Unknown"

    if len(swing_lows) >= 2:

        recent_lows = swing_lows[-3:]

        support_low = min(recent_lows)
        support_high = max(recent_lows)

        support_zone = (
            f"{round(support_low,2)}"
            f" - "
            f"{round(support_high,2)}"
        )

    return {
        "resistance_zone": resistance_zone,
        "support_zone": support_zone
    }