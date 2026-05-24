def analyze_mtf_alignment(
    structure_5m,
    structure_15m,
    structure_1h
):

    trends = [
        structure_5m["trend"],
        structure_15m["trend"],
        structure_1h["trend"]
    ]

    bullish_count = trends.count("Bullish")
    bearish_count = trends.count("Bearish")

    alignment = "Mixed"

    if bullish_count >= 2:
        alignment = "Bullish Alignment"

    elif bearish_count >= 2:
        alignment = "Bearish Alignment"

    strength = "Weak"

    if bullish_count == 3 or bearish_count == 3:
        strength = "Strong"

    elif bullish_count == 2 or bearish_count == 2:
        strength = "Moderate"

    return {
        "5m": structure_5m["trend"],
        "15m": structure_15m["trend"],
        "1h": structure_1h["trend"],
        "alignment": alignment,
        "strength": strength
    }