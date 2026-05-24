def calculate_scores(
    structure,
    oi_direction,
    liquidity
):

    bullish_score = 0
    bearish_score = 0

    trap_risk = "Low"

    trend = structure["trend"]

    # ---------- TREND ---------- #

    if trend == "Bullish":
        bullish_score += 3

    elif trend == "Bearish":
        bearish_score += 3

    # ---------- OI ---------- #

    if oi_direction == "rising":

        bullish_score += 2
        bearish_score += 2

    elif oi_direction == "falling":

        trap_risk = "Medium"

    # ---------- LIQUIDITY ---------- #

    if "Bullish" in liquidity:

        bullish_score += 3

    elif "Bearish" in liquidity:

        bearish_score += 3

    # ---------- QUALITY ---------- #

    difference = abs(
        bullish_score - bearish_score
    )

    quality = "Weak"

    if difference >= 5:
        quality = "A"

    elif difference >= 3:
        quality = "B"

    elif difference >= 2:
        quality = "C"

    # ---------- BIAS ---------- #

    if bullish_score > bearish_score:

        bias = "Bullish"

    elif bearish_score > bullish_score:

        bias = "Bearish"

    else:

        bias = "Neutral"

    return {
        "bullish_score": bullish_score,
        "bearish_score": bearish_score,
        "bias": bias,
        "trap_risk": trap_risk,
        "quality": quality
    }