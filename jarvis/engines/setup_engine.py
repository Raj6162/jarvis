def classify_setup(
    mtf_analysis,
    volume_analysis,
    liquidity,
    oi_analysis,
    structure
):

    setup = "Neutral Conditions"

    confidence = "Low"

    probability = "Weak"

    trend = structure["trend"]

    alignment = mtf_analysis["alignment"]

    volume_state = volume_analysis["state"]

    oi_direction = oi_analysis["direction"]

    # ---------- STRONG BULLISH ---------- #

    if (
        trend == "Bullish"
        and alignment == "Bullish Alignment"
        and oi_direction == "rising"
        and volume_state == "High"
    ):

        setup = "Bullish Continuation"

        confidence = "High"

        probability = "Strong"

    # ---------- STRONG BEARISH ---------- #

    elif (
        trend == "Bearish"
        and alignment == "Bearish Alignment"
        and oi_direction == "rising"
        and volume_state == "High"
    ):

        setup = "Bearish Continuation"

        confidence = "High"

        probability = "Strong"

    # ---------- TRAP CONDITIONS ---------- #

    elif (
        "sweep" in liquidity.lower()
        and volume_state == "Low"
    ):

        setup = "Trap / Liquidity Grab"

        confidence = "Medium"

        probability = "Unstable"

    # ---------- SHORT COVERING ---------- #

    elif (
        oi_direction == "falling"
        and trend == "Bullish"
    ):

        setup = "Short Covering Rally"

        confidence = "Medium"

        probability = "Weak Continuation"

    # ---------- LONG LIQUIDATION ---------- #

    elif (
        oi_direction == "falling"
        and trend == "Bearish"
    ):

        setup = "Long Liquidation"

        confidence = "Medium"

        probability = "Weak Continuation"

    return {
        "setup": setup,
        "confidence": confidence,
        "probability": probability
    }