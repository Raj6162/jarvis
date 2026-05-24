def analyze_oi(oi_data):

    if len(oi_data) < 2:
        return {
            "direction": "neutral",
            "change_percent": 0,
            "interpretation": "Not enough OI data"
        }

    first = float(oi_data[0]["sumOpenInterest"])
    last = float(oi_data[-1]["sumOpenInterest"])

    change = last - first
    percent = (change / first) * 100

    direction = "neutral"
    interpretation = "No major positioning shift"

    if percent > 0.05:
        direction = "rising"
        interpretation = "New positions entering market"

    elif percent < -0.05:
        direction = "falling"
        interpretation = "Positions closing / possible profit taking"

    return {
        "first_oi": round(first, 2),
        "last_oi": round(last, 2),
        "change_percent": round(percent, 2),
        "direction": direction,
        "interpretation": interpretation
    }
def interpret_price_oi(price_change, oi_direction):

    if price_change > 0 and oi_direction == "rising":
        return "Bullish continuation likely (new longs entering)"

    elif price_change > 0 and oi_direction == "falling":
        return "Short covering rally possible"

    elif price_change < 0 and oi_direction == "rising":
        return "Bearish continuation likely (new shorts entering)"

    elif price_change < 0 and oi_direction == "falling":
        return "Long liquidation / profit taking"

    return "Neutral market conditions"