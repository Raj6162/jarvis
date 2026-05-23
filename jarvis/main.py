import requests
import os

from engines.session_engine import detect_session

from dotenv import load_dotenv

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

from engines.sr_engine import detect_sr

from engines.mtf_engine import analyze_mtf_alignment

from api.binance_client import (
    fetch_klines,
    fetch_open_interest
)

from engines.oi_engine import (
    analyze_oi,
    interpret_price_oi
)

from engines.structure_engine import detect_structure

from engines.liquidity_engine import (
    detect_liquidity_sweep,
    detect_fvg
)

from engines.scoring_engine import calculate_scores

from engines.volume_engine import analyze_volume

# ---------------- ENV ---------------- #

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
TWELVE_API_KEY = os.getenv("TWELVE_API_KEY")

# ---------------- USER STATE ---------------- #

user_state = {}

# ---------------- ASSETS ---------------- #

CRYPTO = {
    "BTC": "BTCUSDT",
    "ETH": "ETHUSDT",
    "SOL": "SOLUSDT"
}

TIMEFRAMES = ["5m", "15m"]

MTF = ["5m", "15m", "1h", "4h", "1d"]

LIMITS = {
    "5m": 60,
    "15m": 40,
    "1h": 25,
    "4h": 12,
    "1d": 5
}

# ---------------- TWELVE DATA ---------------- #

def fetch_twelve(symbol, tf, limit):

    tf_map = {
        "5m": "5min",
        "15m": "15min",
        "1h": "1h",
        "4h": "4h",
        "1d": "1day"
    }

    url = (
        f"https://api.twelvedata.com/time_series?"
        f"symbol={symbol}"
        f"&interval={tf_map[tf]}"
        f"&apikey={TWELVE_API_KEY}"
        f"&outputsize={limit}"
    )

    data = requests.get(url).json()

    if "values" not in data:
        raise Exception(data.get("message", "API error"))

    candles = []

    for c in reversed(data["values"]):

        candles.append((
            round(float(c["open"]), 2),
            round(float(c["high"]), 2),
            round(float(c["low"]), 2),
            round(float(c["close"]), 2)
        ))

    return candles

# ---------------- FORMAT ---------------- #

def compress(candles):

    formatted = []

    for candle in candles:

        o = candle[0]
        h = candle[1]
        l = candle[2]
        c = candle[3]

        formatted.append(
            f"{o},{h},{l},{c}"
        )

    return ";".join(formatted)

# ---------------- OHLCV OUTPUT ---------------- #

def build_ohlcv_output(asset, selected_tf, all_data):

    text = f"ASSET:{asset} TF:{selected_tf}\n\n"

    ordered = [selected_tf] + [
        t for t in MTF if t != selected_tf
    ]

    for tf in ordered:

        candles = all_data[tf]

        text += f"{tf}:\n"
        text += f"{compress(candles)}\n\n"

    return text[:3800]

# ---------------- SUMMARY OUTPUT ---------------- #

def build_summary_output(
    oi_analysis,
    market_interpretation,
    structure,
    liquidity,
    fvg,
    scores,
    volume_analysis,
    session_analysis,
    sr_analysis,
    mtf_analysis
):

    text = ""

    text += "=== MARKET INTELLIGENCE ===\n\n"

    # ---------- OI ---------- #

    text += "OI Analysis:\n"
    text += f"Direction: {oi_analysis['direction']}\n"
    text += f"Change: {oi_analysis['change_percent']}%\n"
    text += f"{oi_analysis['interpretation']}\n\n"

    # ---------- MARKET ---------- #

    text += "Market Interpretation:\n"
    text += f"{market_interpretation}\n\n"

    # ---------- STRUCTURE ---------- #

    text += "Structure Analysis:\n"
    text += f"Trend: {structure['trend']}\n"
    text += f"BOS: {structure['bos']}\n"
    text += f"CHOCH: {structure['choch']}\n\n"

    # ---------- LIQUIDITY ---------- #

    text += "Liquidity Analysis:\n"
    text += f"{liquidity}\n\n"

    # ---------- FVG ---------- #

    text += "FVG Analysis:\n"
    text += f"{fvg}\n\n"

    # ---------- CONFLUENCE ---------- #

    text += "Confluence Analysis:\n"
    text += f"Bullish Score: {scores['bullish_score']}/10\n"
    text += f"Bearish Score: {scores['bearish_score']}/10\n"
    text += f"Bias: {scores['bias']}\n"
    text += f"Trap Risk: {scores['trap_risk']}\n\n"

    # ---------- VOLUME ---------- #

    text += "Volume Analysis:\n"
    text += f"State: {volume_analysis['state']}\n"
    text += f"Ratio: {volume_analysis['ratio']}\n"
    text += f"{volume_analysis['message']}\n"
    text += "\nSession Analysis:\n"
    text += f"Current Session: {session_analysis['session']}\n"
    text += f"Volatility: {session_analysis['volatility']}\n"
    text += f"{session_analysis['message']}\n"
    text += "\nSupport & Resistance:\n"
    text += f"Resistance: {sr_analysis['resistance']}\n"
    text += f"Support: {sr_analysis['support']}\n"
    text += "\nMTF Alignment:\n"
    text += f"5m Trend: {mtf_analysis['5m']}\n"
    text += f"15m Trend: {mtf_analysis['15m']}\n"
    text += f"1h Trend: {mtf_analysis['1h']}\n"
    text += f"Alignment: {mtf_analysis['alignment']}\n"
    text += f"Strength: {mtf_analysis['strength']}\n"

    return text[:3500]

# ---------------- KEYBOARDS ---------------- #

def asset_keyboard():

    return ReplyKeyboardMarkup(
        [
            ["BTC", "ETH", "SOL"]
        ],
        resize_keyboard=True
    )

def tf_keyboard():

    return ReplyKeyboardMarkup(
        [TIMEFRAMES],
        resize_keyboard=True
    )

# ---------------- START ---------------- #

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_state[update.effective_user.id] = {
        "step": "asset"
    }

    await update.message.reply_text(
        "Select Asset:",
        reply_markup=asset_keyboard()
    )

# ---------------- HANDLE ---------------- #

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    uid = update.effective_user.id
    text = update.message.text.strip().upper()

    if text == "START":
        return await start(update, context)

    state = user_state.get(uid, {})

    # ---------- STEP 1 : ASSET ---------- #

    if state.get("step") == "asset":

        if text not in CRYPTO:

            return await update.message.reply_text(
                "Use buttons.",
                reply_markup=asset_keyboard()
            )

        user_state[uid] = {
            "step": "tf",
            "asset": text
        }

        await update.message.reply_text(
            f"{text} selected\nChoose timeframe:",
            reply_markup=tf_keyboard()
        )

    # ---------- STEP 2 : TIMEFRAME ---------- #

    elif state.get("step") == "tf":

        tf = text.lower()

        if tf not in TIMEFRAMES:

            return await update.message.reply_text(
                "Select valid TF.",
                reply_markup=tf_keyboard()
            )

        asset = state["asset"]

        await update.message.reply_text(
            "Fetching data..."
        )

        try:

            all_data = {}

            # ---------- FETCH OHLCV ---------- #

            for t in MTF:

                limit = LIMITS[t]

                candles_raw = fetch_klines(
                    CRYPTO[asset],
                    t,
                    limit
                )

                candles = []

                for c in candles_raw:

                    candles.append((
                        round(c["open"], 2),
                        round(c["high"], 2),
                        round(c["low"], 2),
                        round(c["close"], 2),
                        round(c["volume"], 2)
                    ))

                all_data[t] = candles

            # ---------- OI ---------- #

            oi_data = fetch_open_interest(
                CRYPTO[asset]
            )

            oi_analysis = analyze_oi(oi_data)

            # ---------- PRICE + OI ---------- #

            latest_5m = all_data["5m"]

            first_close = latest_5m[0][3]
            last_close = latest_5m[-1][3]

            price_change = last_close - first_close

            market_interpretation = interpret_price_oi(
                price_change,
                oi_analysis["direction"]
            )

            # ---------- STRUCTURE ---------- #

            structure_5m = detect_structure(
                all_data["5m"]
            )

            structure_15m = detect_structure(
                all_data["15m"]
            )

            structure_1h = detect_structure(
                all_data["1h"]
            )

            # Main structure for scoring compatibility

            structure = structure_5m

            # ---------- LIQUIDITY ---------- #

            liquidity = detect_liquidity_sweep(
                all_data["5m"]
            )

            # ---------- FVG ---------- #

            fvg = detect_fvg(
                all_data["5m"]
            )

            # ---------- SCORES ---------- #

            scores = calculate_scores(
                structure,
                oi_analysis["direction"],
                liquidity
            )

            # ---------- VOLUME ---------- #

            volume_analysis = analyze_volume(
                all_data["5m"]
            )
            
            session_analysis = detect_session()

            sr_analysis = detect_sr(
                all_data["15m"]
            )
            mtf_analysis = analyze_mtf_alignment(
                structure_5m,
                structure_15m,
                structure_1h
            )

            
            # ---------- BUILD OUTPUTS ---------- #

            summary_output = build_summary_output(
                oi_analysis,
                market_interpretation,
                structure,
                liquidity,
                fvg,
                scores,
                volume_analysis,
                session_analysis,
                sr_analysis,
                mtf_analysis
            )

            ohlcv_output = build_ohlcv_output(
                asset,
                tf,
                all_data
            )

            # ---------- SEND SUMMARY ---------- #

            await update.message.reply_text(
                summary_output
            )

            # ---------- SEND OHLCV ---------- #

            await update.message.reply_text(
                ohlcv_output
            )

            # ---------- RESET ---------- #

            user_state[uid] = {
                "step": "asset"
            }

            await update.message.reply_text(
                "Select next asset:",
                reply_markup=asset_keyboard()
            )

        except Exception as e:

            await update.message.reply_text(
                f"Error: {e}"
            )

# ---------------- RUN ---------------- #

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle
    )
)

print("Jarvis running...")

app.run_polling()