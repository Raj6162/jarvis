def analyze_volume(candles):

    try:

        if len(candles) < 6:
            return {
                "state": "Unknown",
                "ratio": 0,
                "message": "Not enough volume data"
            }

        volumes = []

        for c in candles:
            volumes.append(c[4])

        recent_volume = volumes[-1]

        avg_volume = sum(volumes[:-1]) / len(volumes[:-1])

        ratio = recent_volume / avg_volume

        if ratio > 1.5:
            state = "High"
            message = "Strong volume expansion detected"

        elif ratio < 0.7:
            state = "Low"
            message = "Weak participation / low conviction"

        else:
            state = "Normal"
            message = "Average market participation"

        return {
            "state": state,
            "ratio": round(ratio, 2),
            "message": message
        }

    except Exception as e:

        return {
            "state": "Error",
            "ratio": 0,
            "message": str(e)
        }