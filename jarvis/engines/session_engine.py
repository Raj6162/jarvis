from datetime import datetime
import pytz


def detect_session():

    utc_now = datetime.now(pytz.utc)

    hour = utc_now.hour

    # ---------- ASIAN ---------- #

    if 0 <= hour < 7:

        return {
            "session": "Asian",
            "volatility": "Low",
            "message": "Ranging / lower volatility conditions"
        }

    # ---------- LONDON ---------- #

    elif 7 <= hour < 13:

        return {
            "session": "London",
            "volatility": "High",
            "message": "High probability expansion session"
        }

    # ---------- NEW YORK ---------- #

    elif 13 <= hour < 21:

        return {
            "session": "New York",
            "volatility": "High",
            "message": "High volatility / institutional activity"
        }

    # ---------- LATE SESSION ---------- #

    return {
        "session": "Late Session",
        "volatility": "Medium",
        "message": "Reduced institutional participation"
    }