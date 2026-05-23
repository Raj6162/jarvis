def detect_sr(candles):

    if len(candles) < 10:

        return {
            "resistance": "Unknown",
            "support": "Unknown"
        }

    highs = [c[1] for c in candles]
    lows = [c[2] for c in candles]

    resistance = max(highs[-10:])
    support = min(lows[-10:])

    return {
        "resistance": round(resistance, 2),
        "support": round(support, 2)
    }