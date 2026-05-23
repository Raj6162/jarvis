def calculate_scores(
    structure,
    oi_direction,
    liquidity
):

    bullish_score = 0
    bearish_score = 0
    trap_risk = "Low"

    # ---------- Structure ---------- #

    if "Bullish" in structure:
        bullish_score += 3

    elif "Bearish" in structure:
        bearish_score += 3

    # ---------- OI ---------- #

    if oi_direction == "rising":
        bullish_score += 2

    elif oi_direction == "falling":
        bearish_score += 1

    # ---------- Liquidity ---------- #

    if "Bullish" in liquidity:
        bullish_score += 3
        trap_risk = "Medium"

    elif "Bearish" in liquidity:
        bearish_score += 3
        trap_risk = "Medium"

    # ---------- Final Bias ---------- #

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
        "trap_risk": trap_risk
    }