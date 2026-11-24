# =============================================================================
# ⚡ GLOBAL VPS & BOT HOSTING STORE BOT (100% ENGLISH + 100+ WORLD LANGUAGES)
# =============================================================================
import os
import html
import json
import time
import uuid
import asyncio
from datetime import datetime

import aiohttp
from aiohttp import web
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# 1. CONFIGURATION (SET IN RENDER ENVIRONMENT VARIABLES OR .env)
# =============================================================================
BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()
OWNER_ID = int(os.environ.get("OWNER_ID", "0"))
BACKUP_CHANNEL = int(os.environ.get("BACKUP_CHANNEL", "0"))

STORE_NAME = os.environ.get("STORE_NAME", "FlyTon Cloud Store")
SUPPORT_USER = os.environ.get("SUPPORT_USER", "@YourSupportID")
PROOF_CHANNEL_URL = os.environ.get("PROOF_CHANNEL_URL", "https://t.me/YourChannel")
DEFAULT_UPI_ID = os.environ.get("UPI_ID", "yourupi@fam")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "store_db.json")

DEFAULT_PLANS = {
    "panel_1gb": {
        "category": "panel",
        "name": "Starter Bot Panel (1 GB RAM)",
        "specs": "1 GB RAM • 100% CPU • 10 GB SSD • Python/Node Ready",
        "inr": 100,
        "stars": 75,
        "days": 30,
    },
    "panel_2gb": {
        "category": "panel",
        "name": "Pro Bot Panel (2 GB RAM)",
        "specs": "2 GB RAM • 150% CPU • 20 GB SSD • 24/7 Non-Stop",
        "inr": 160,
        "stars": 120,
        "days": 30,
    },
    "panel_4gb": {
        "category": "panel",
        "name": "Ultra Bot Panel (4 GB RAM)",
        "specs": "4 GB RAM • 200% CPU • 40 GB SSD • Multi-Bot Support",
        "inr": 250,
        "stars": 185,
        "days": 30,
    },
    "vps_4gb": {
        "category": "vps",
        "name": "Basic Ubuntu VPS (4 GB RAM)",
        "specs": "2 vCPU • 4 GB RAM • 50 GB NVMe • Full Root Access",
        "inr": 450,
        "stars": 330,
        "days": 30,
    },
    "vps_8gb": {
        "category": "vps",
        "name": "Power Ubuntu VPS (8 GB RAM)",
        "specs": "4 vCPU • 8 GB RAM • 100 GB NVMe • Full Root + FFmpeg",
        "inr": 750,
        "stars": 550,
        "days": 30,
    },
}

# =============================================================================
# 2. 100+ WORLD LANGUAGES & LIVE TRANSLATION ENGINE (ZERO EXTRA PACKAGES)
# =============================================================================
WORLD_LANGUAGES = {
    "en": "🇺🇸 English",
    "hi": "🇮🇳 Hindi (हिन्दी)",
    "es": "🇪🇸 Spanish (Español)",
    "ar": "🇸🇦 Arabic (العربية)",
    "ru": "🇷🇺 Russian (Русский)",
    "id": "🇮🇩 Indonesian",
    "pt": "🇧🇷 Portuguese",
    "fr": "🇫🇷 French (Français)",
    "de": "🇩🇪 German (Deutsch)",
    "tr": "🇹🇷 Turkish (Türkçe)",
    "zh-CN": "🇨🇳 Chinese Simplified",
    "zh-TW": "🇹🇼 Chinese Traditional",
    "ja": "🇯🇵 Japanese (日本語)",
    "ko": "🇰🇷 Korean (한국어)",
    "vi": "🇻🇳 Vietnamese",
    "bn": "🇧🇩 Bengali (বাংলা)",
    "ur": "🇵🇰 Urdu (اردو)",
    "it": "🇮🇹 Italian (Italiano)",
    "th": "🇹🇭 Thai (ไทย)",
    "tl": "🇵🇭 Filipino / Tagalog",
    "fa": "🇮🇷 Persian (فارسی)",
    "uk": "🇺🇦 Ukrainian",
    "pl": "🇵🇱 Polish (Polski)",
    "nl": "🇳🇱 Dutch (Nederlands)",
    "ms": "🇲🇾 Malay (Melayu)",
    "ta": "🇮🇳 Tamil (தமிழ்)",
    "te": "🇮🇳 Telugu (తెలుగు)",
    "mr": "🇮🇳 Marathi (मराठी)",
    "gu": "🇮🇳 Gujarati (ગુજરાતી)",
    "pa": "🇮🇳 Punjabi (ਪੰਜਾਬੀ)",
    "kn": "🇮🇳 Kannada (ಕನ್ನಡ)",
    "ml": "🇮🇳 Malayalam (മലയാളം)",
    "as": "🇮🇳 Assamese (অসমীয়া)",
    "or": "🇮🇳 Odia (ଓଡ଼ିଆ)",
    "ne": "🇳🇵 Nepali (नेपाली)",
    "si": "🇱🇰 Sinhala",
    "my": "🇲🇲 Burmese (Myanmar)",
    "km": "🇰🇭 Khmer",
    "lo": "🇱🇦 Lao",
    "uz": "🇺🇿 Uzbek",
    "kk": "🇰🇿 Kazakh",
    "az": "🇦🇿 Azerbaijani",
    "ky": "🇰🇬 Kyrgyz",
    "tg": "🇹🇯 Tajik",
    "tk": "🇹🇲 Turkmen",
    "mn": "🇲🇳 Mongolian",
    "ka": "🇬🇪 Georgian",
    "hy": "🇦🇲 Armenian",
    "he": "🇮🇱 Hebrew",
    "ps": "🇦🇫 Pashto",
    "ku": "🇮🇶 Kurdish",
    "ro": "🇷🇴 Romanian",
    "cs": "🇨🇿 Czech",
    "el": "🇬🇷 Greek",
    "sv": "🇸🇪 Swedish",
    "da": "🇩🇰 Danish",
    "fi": "🇫🇮 Finnish",
    "no": "🇳🇴 Norwegian",
    "hu": "🇭🇺 Hungarian",
    "bg": "🇧🇬 Bulgarian",
    "sr": "🇷🇸 Serbian",
    "hr": "🇭🇷 Croatian",
    "sk": "🇸🇰 Slovak",
    "sl": "🇸🇮 Slovenian",
    "lt": "🇱🇹 Lithuanian",
    "lv": "🇱🇻 Latvian",
    "et": "🇪🇪 Estonian",
    "sq": "🇦🇱 Albanian",
    "bs": "🇧🇦 Bosnian",
    "mk": "🇲🇰 Macedonian",
    "be": "🇧🇾 Belarusian",
    "ca": "🇪🇸 Catalan",
    "eu": "🇪🇸 Basque",
    "gl": "🇪🇸 Galician",
    "ga": "🇮🇪 Irish",
    "cy": "🏴󠁧󠁢󠁷󠁬󠁳󠁿 Welsh",
    "is": "🇮🇸 Icelandic",
    "mt": "🇲🇹 Maltese",
    "sw": "🇰🇪 Swahili",
    "am": "🇪🇹 Amharic",
    "ha": "🇳🇬 Hausa",
    "yo": "🇳🇬 Yoruba",
    "ig": "🇳🇬 Igbo",
    "zu": "🇿🇦 Zulu",
    "xh": "🇿🇦 Xhosa",
    "af": "🇿🇦 Afrikaans",
    "so": "🇸🇴 Somali",
    "rw": "🇷🇼 Kinyarwanda",
    "mg": "🇲🇬 Malagasy",
    "sn": "🇿🇼 Shona",
    "st": "🇱🇸 Sesotho",
    "ny": "🇲🇼 Chichewa",
    "om": "🇪🇹 Oromo",
    "ti": "🇪🇷 Tigrinya",
    "ht": "🇭🇹 Haitian Creole",
    "qu": "🇵🇪 Quechua",
    "gn": "🇵🇾 Guarani",
    "jv": "🇮🇩 Javanese",
    "su": "🇮🇩 Sundanese",
    "ceb": "🇵🇭 Cebuano",
    "mi": "🇳🇿 Maori",
    "sm": "🇼🇸 Samoan",
    "haw": "🇺🇸 Hawaiian",
    "eo": "🌐 Esperanto",
    "la": "🏛 Latin",
}

# All UI strings in pure English (single-line for 100% clean translation)
BASE_STRINGS = {
    "welcome": "Welcome",
    "home_desc": "Get 24/7 high-speed Bot Hosting Panels and Full Root Ubuntu VPS servers at the best prices worldwide.",
    "lbl_payments": "Payments",
    "val_payments": "Telegram Stars (Global) & UPI (India)",
    "lbl_delivery": "Delivery",
    "val_delivery": "Instant / Fast Provisioning",
    "lbl_active_plans": "Your Active Plans",
    "home_tip": "Choose a service or change your language below:",
    "btn_panels": "🤖 Bot Hosting Panels",
    "btn_vps": "🖥 Full Root VPS",
    "btn_services": "📦 My Services",
    "btn_orders": "🧾 My Orders",
    "btn_rules": "📜 Rules & Terms",
    "btn_support": "💬 Support",
    "btn_language": "🌐 Language",
    "btn_proof": "📢 Proof & Updates Channel",
    "btn_admin": "👑 Owner Admin Dashboard",
    "btn_back_home": "🔙 Back to Main Menu",
    "btn_back_plans": "🔙 Back to Plans",
    "btn_cancel_pay": "❌ Cancel Payment",
    "btn_renew": "🔄 Renew Now",
    "btn_order_again": "🛒 Order Again",
    "btn_buy": "Buy",
    "cat_panel_title": "BOT HOSTING PANELS (24/7)",
    "cat_panel_desc": "Non-stop 24/7 panels for Python, Node.js, and Telegram bots with easy mobile control.",
    "cat_vps_title": "FULL ROOT UBUNTU VPS",
    "cat_vps_desc": "Dedicated root Linux servers for FFmpeg, encoding, multi-bots, and heavy automation.",
    "badge_instant": "Instant Stock",
    "badge_fast": "Fast Setup",
    "no_plans": "No plans available in this category yet.",
    "lbl_status": "Status",
    "lbl_days": "Days",
    "lbl_stars": "Stars",
    "checkout_title": "ORDER CHECKOUT",
    "lbl_plan": "Plan",
    "lbl_specs": "Specs",
    "lbl_validity": "Validity",
    "lbl_upi_price": "UPI Price (India)",
    "lbl_stars_price": "Stars Price (Global)",
    "deliv_instant": "Instant Auto-Delivery (Stock Ready)",
    "deliv_manual": "Fast Manual Setup (5-15 mins)",
    "choose_pay": "Select your preferred payment method below:",
    "btn_pay_stars": "Pay with Telegram Stars (Worldwide)",
    "btn_pay_upi": "Pay via UPI / QR (India)",
    "upi_title": "UPI PAYMENT (INDIA)",
    "lbl_exact_amt": "Pay Exact Amount",
    "lbl_upi_id": "UPI ID (Tap to Copy)",
    "upi_next_step": "After payment, send the payment screenshot (and optional UTR number) directly in this chat. Your server will be delivered once verified.",
    "ss_received_title": "SCREENSHOT RECEIVED",
    "ss_received_desc": "Admin is verifying your payment. Your server credentials will be sent here right after approval.",
    "my_services_title": "MY ACTIVE SERVICES",
    "no_services": "You do not have any active VPS or Bot Panel yet.",
    "days_left": "Days Left",
    "expired": "Expired",
    "valid_till": "Valid Till",
    "my_orders_title": "RECENT ORDERS",
    "no_orders": "You have not placed any orders yet.",
    "rules_title": "TERMS & RULES",
    "rule_1": "No Illegal Use: Crypto mining, DDoS, port scanning, or spamming will result in immediate suspension with no refund.",
    "rule_2": "No Fake Proofs: Sending fake payment screenshots will result in a permanent ban from the store.",
    "rule_3": "Timely Renewal: Renewal reminders are sent 3 days before expiry. Unrenewed servers may be deleted after expiry.",
    "rule_4": "Support: Contact our official support account anytime for setup help or technical issues.",
    "server_ready_title": "YOUR SERVER IS READY",
    "lbl_order_id": "Order ID",
    "lbl_login_details": "LOGIN DETAILS (Tap to Copy)",
    "rule_note": "Please change your password after first login. Mining, DDoS, and spamming are strictly prohibited.",
    "pay_confirmed_title": "PAYMENT CONFIRMED",
    "pay_confirmed_desc": "Your server is being provisioned right now. Your login credentials will arrive here within a few minutes.",
    "pay_rejected_title": "PAYMENT REJECTED",
    "pay_rejected_desc": "Your UPI payment could not be verified. If money was deducted, please contact support with your UTR number.",
    "renew_title": "RENEWAL REMINDER",
    "renew_desc": "Your server is expiring soon. Please renew on time to keep your files and bots running safely.",
    "expired_title": "PLAN EXPIRED",
    "expired_desc": "Your server validity has ended. Place a new order to reactivate or purchase a fresh server.",
    "lang_title": "SELECT YOUR LANGUAGE",
    "lang_desc": "Choose from 100+ world languages below, or tap Search to type any language name or code.",
    "btn_lang_search": "🔎 Type Any Language Name",
    "btn_prev": "⬅️ Previous",
    "btn_next": "Next ➡️",
    "lang_search_prompt": "Type any language name or ISO code (Examples: Japanese, Spanish, Arabic, Hindi, Russian, Tamil, fr, de, tr):",
    "lang_changed": "Language updated successfully!",
    "lang_not_found": "Language not recognized. Please pick from the menu or type a valid language name like French, Arabic, or Hindi.",
}

LANG_CACHE = {"en": dict(BASE_STRINGS)}
LANG_LOCKS = {}

# =============================================================================
# 3. DATABASE ENGINE (PERSISTENT JSON + BACKUP / RESTORE)
# =============================================================================
db = {
    "users": {},
    "plans": json.loads(json.dumps(DEFAULT_PLANS)),
    "stock": {},
    "orders": {},
    "settings": {
        "upi_id": DEFAULT_UPI_ID,
        "qr_file_id": "",
        "support": SUPPORT_USER,
        "proof_url": PROOF_CHANNEL_URL,
    },
}

pending_upi_proof = {}   # {uid_str: order_id}
await_lang_input = set() # {uid_str}
http_session: aiohttp.ClientSession = None
_shutdown = False


def load_db():
    global db
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                for k in ("users", "plans", "stock", "orders", "settings"):
                    if k in loaded:
                        db[k] = loaded[k]
        except Exception as e:
            print(f"[DB Load Warning] {e}")

    if not db.get("plans"):
        db["plans"] = json.loads(json.dumps(DEFAULT_PLANS))
    db["settings"].setdefault("upi_id", DEFAULT_UPI_ID)
    db["settings"].setdefault("qr_file_id", "")
    db["settings"].setdefault("support", SUPPORT_USER)
    db["settings"].setdefault("proof_url", PROOF_CHANNEL_URL)


def save_db():
    try:
        tmp = DB_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=2, ensure_ascii=False)
        os.replace(tmp, DB_FILE)
    except Exception as e:
        print(f"[DB Save Warning] {e}")


def esc(val) -> str:
    return html.escape(str(val if val is not None else ""))


def is_owner(uid: int) -> bool:
    return uid == OWNER_ID


def register_user(user: dict):
    if not user:
        return
    uid = str(user["id"])
    name = (user.get("first_name") or "User").strip()
    uname = user.get("username") or ""
    if uid not in db["users"]:
        db["users"][uid] = {
            "name": name,
            "username": uname,
            "lang": "en",
            "joined": int(time.time()),
        }
        save_db()
    else:
        db["users"][uid]["name"] = name
        db["users"][uid]["username"] = uname
        db["users"][uid].setdefault("lang", "en")


def get_user_lang(uid: int) -> str:
    return db.get("users", {}).get(str(uid), {}).get("lang", "en") or "en"


def set_user_lang(uid: int, lang_code: str):
    uid_s = str(uid)
    db["users"].setdefault(uid_s, {"name": "User", "username": "", "joined": int(time.time())})
    db["users"][uid_s]["lang"] = lang_code
    save_db()


def days_left(expires_at: float) -> int:
    if not expires_at:
        return 0
    return max(0, int((expires_at - time.time()) // 86400) + 1) if expires_at > time.time() else 0


def fmt_date(ts: float) -> str:
    if not ts:
        return "N/A"
    return datetime.fromtimestamp(ts).strftime("%d %b %Y")


def stock_count(plan_key: str) -> int:
    return len(db.get("stock", {}).get(plan_key, []))


async def _translate_chunk(texts: list, target_lang: str) -> list:
    if target_lang == "en":
        return texts
    url = "https://translate.googleapis.com/translate_a/single"
    params = {"client": "gtx", "sl": "en", "tl": target_lang, "dt": "t"}
    try:
        async with http_session.post(
            url,
            params=params,
            data={"q": "\n".join(texts)},
            timeout=aiohttp.ClientTimeout(total=15),
        ) as resp:
            if resp.status == 200:
                data = await resp.json(content_type=None)
                full = "".join(seg[0] for seg in data[0] if seg and seg[0])
                lines = [ln.strip() for ln in full.strip().split("\n")]
                if len(lines) == len(texts):
                    return lines
    except Exception as e:
        print(f"[Translate Warning] {target_lang}: {e}")
    return texts


async def get_pack(lang_code: str) -> dict:
    code = (lang_code or "en").strip()
    if code in LANG_CACHE:
        return LANG_CACHE[code]

    lock = LANG_LOCKS.setdefault(code, asyncio.Lock())
    async with lock:
        if code in LANG_CACHE:
            return LANG_CACHE[code]
        keys = list(BASE_STRINGS.keys())
        vals = [BASE_STRINGS[k] for k in keys]
        translated_all = []
        chunk_size = 18
        for i in range(0, len(vals), chunk_size):
            chunk = vals[i:i + chunk_size]
            res = await _translate_chunk(chunk, code)
            translated_all.extend(res)
        pack = {k: (v if v else BASE_STRINGS[k]) for k, v in zip(keys, translated_all)}
        LANG_CACHE[code] = pack
        return pack


def resolve_language_query(query: str):
    q = query.strip().lower()
    if not q:
        return None
    # Exact ISO code match
    for code in WORLD_LANGUAGES:
        if code.lower() == q:
            return code
    # Partial match against display label
    for code, label in WORLD_LANGUAGES.items():
        if q in label.lower():
            return code
    # Allow any valid 2-letter ISO code directly (e.g., 'gl', 'sd', 'tt', 'ug')
    if len(q) == 2 and q.isalpha():
        return q
    return None


# =============================================================================
# 4. TELEGRAM BOT API ENGINE (COLORFUL BUTTONS + STARS INVOICE)
# =============================================================================
async def tg_call(method: str, payload: dict = None, form: aiohttp.FormData = None) -> dict:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"
    try:
        if form is not None:
            async with http_session.post(url, data=form, timeout=aiohttp.ClientTimeout(total=45)) as resp:
                return await resp.json()
        async with http_session.post(url, json=payload or {}, timeout=aiohttp.ClientTimeout(total=45)) as resp:
            return await resp.json()
    except Exception as e:
        print(f"[TG API Error] {method}: {e}")
        return {"ok": False, "description": str(e)}


def _strip_styles(rows: list) -> list:
    return [[{k: v for k, v in b.items() if k != "style"} for b in row] for row in rows]


async def send_msg(chat_id: int, text: str, buttons: list = None, reply_to: int = None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    if reply_to:
        payload["reply_to_message_id"] = reply_to
    if buttons:
        payload["reply_markup"] = {"inline_keyboard": buttons}

    res = await tg_call("sendMessage", payload)
    if not res.get("ok") and buttons:
        payload["reply_markup"] = {"inline_keyboard": _strip_styles(buttons)}
        res = await tg_call("sendMessage", payload)
    return res


async def edit_msg(chat_id: int, message_id: int, text: str, buttons: list = None):
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    if buttons:
        payload["reply_markup"] = {"inline_keyboard": buttons}

    res = await tg_call("editMessageText", payload)
    if not res.get("ok") and buttons:
        desc = (res.get("description") or "").lower()
        if "message is not modified" in desc:
            return res
        payload["reply_markup"] = {"inline_keyboard": _strip_styles(buttons)}
        res = await tg_call("editMessageText", payload)
    return res


async def send_photo(chat_id: int, photo: str, caption: str, buttons: list = None):
    payload = {
        "chat_id": chat_id,
        "photo": photo,
        "caption": caption,
        "parse_mode": "HTML",
    }
    if buttons:
        payload["reply_markup"] = {"inline_keyboard": buttons}

    res = await tg_call("sendPhoto", payload)
    if not res.get("ok") and buttons:
        payload["reply_markup"] = {"inline_keyboard": _strip_styles(buttons)}
        res = await tg_call("sendPhoto", payload)
    return res


async def delete_msg(chat_id: int, message_id: int):
    await tg_call("deleteMessage", {"chat_id": chat_id, "message_id": message_id})


async def answer_cb(cb_id: str, text: str = "", alert: bool = False):
    await tg_call("answerCallbackQuery", {
        "callback_query_id": cb_id,
        "text": text[:190],
        "show_alert": alert,
    })


async def send_stars_invoice(chat_id: int, plan: dict, order_id: str):
    payload = {
        "chat_id": chat_id,
        "title": plan["name"][:32],
        "description": f"{plan['specs']} | Validity: {plan['days']} Days"[:250],
        "payload": order_id,
        "provider_token": "",  # Must remain empty for Telegram Stars (XTR)
        "currency": "XTR",
        "prices": [{"label": f"{plan['days']} Days Access", "amount": int(plan["stars"])}],
    }
    return await tg_call("sendInvoice", payload)


async def send_db_backup(target_chat: int, caption: str):
    save_db()
    if not os.path.exists(DB_FILE):
        return
    form = aiohttp.FormData()
    form.add_field("chat_id", str(target_chat))
    form.add_field("caption", caption)
    form.add_field("parse_mode", "HTML")
    with open(DB_FILE, "rb") as f:
        form.add_field("document", f.read(), filename="store_db.json", content_type="application/json")
    await tg_call("sendDocument", form=form)


# =============================================================================
# 5. RENDER WEB HEALTH SERVER
# =============================================================================
async def start_web_server():
    app = web.Application()

    async def handle_root(request):
        return web.Response(
            text=f"⚡ {STORE_NAME} is Online | Users: {len(db['users'])} | Orders: {len(db['orders'])}"
        )

    async def handle_health(request):
        return web.json_response({
            "status": "ok",
            "store": STORE_NAME,
            "users": len(db["users"]),
            "orders": len(db["orders"]),
            "languages_cached": len(LANG_CACHE),
        })

    app.router.add_get("/", handle_root)
    app.router.add_get("/health", handle_health)

    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", "8080"))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"🌐 Web Server Bound on 0.0.0.0:{port}")
    return runner


# =============================================================================
# 6. HIGH-QUALITY MULTILINGUAL UI BUILDERS (COLORFUL BUTTONS)
# =============================================================================
async def build_home_ui(uid: int, first_name: str):
    lang = get_user_lang(uid)
    t = await get_pack(lang)
    lang_label = WORLD_LANGUAGES.get(lang, f"🌐 {lang.upper()}")

    active_cnt = sum(
        1 for o in db["orders"].values()
        if o["user_id"] == uid and o["status"] == "completed" and o.get("expires_at", 0) > time.time()
    )
    text = (
        f"<blockquote>⚡ <b>{esc(STORE_NAME.upper())}</b> ⚡</blockquote>\n"
        f"<blockquote>"
        f"👋 <b>{esc(t['welcome'])}, {esc(first_name)}!</b>\n"
        f"{esc(t['home_desc'])}\n\n"
        f"╭ 💳 <b>{esc(t['lbl_payments'])}:</b> <code>{esc(t['val_payments'])}</code>\n"
        f"├ ⚡ <b>{esc(t['lbl_delivery'])}:</b> <code>{esc(t['val_delivery'])}</code>\n"
        f"├ 🌐 <b>Language:</b> <code>{esc(lang_label)}</code>\n"
        f"╰ 📦 <b>{esc(t['lbl_active_plans'])}:</b> <code>{active_cnt}</code>"
        f"</blockquote>\n"
        f"<blockquote>👇 {esc(t['home_tip'])}</blockquote>"
    )
    buttons = [
        [
            {"text": t["btn_panels"], "callback_data": "cat_panel", "style": "primary"},
            {"text": t["btn_vps"], "callback_data": "cat_vps", "style": "success"},
        ],
        [
            {"text": t["btn_services"], "callback_data": "my_services", "style": "primary"},
            {"text": t["btn_orders"], "callback_data": "my_orders", "style": "success"},
        ],
        [
            {"text": f"{t['btn_language']} ({lang.upper()})", "callback_data": "lang_menu_0", "style": "primary"},
            {"text": t["btn_rules"], "callback_data": "show_rules", "style": "danger"},
        ],
        [
            {"text": t["btn_support"], "url": f"https://t.me/{db['settings']['support'].lstrip('@')}", "style": "success"},
        ],
    ]
    if db["settings"].get("proof_url", "").startswith("http"):
        buttons[-1].append({"text": t["btn_proof"], "url": db["settings"]["proof_url"], "style": "primary"})
    if is_owner(uid):
        buttons.append([{"text": t["btn_admin"], "callback_data": "adm_home", "style": "danger"}])
    return text, buttons


async def build_category_ui(uid: int, cat: str):
    t = await get_pack(get_user_lang(uid))
    title = f"🤖 {t['cat_panel_title']}" if cat == "panel" else f"🖥 {t['cat_vps_title']}"
    desc = t["cat_panel_desc"] if cat == "panel" else t["cat_vps_desc"]

    text = f"<blockquote><b>{esc(title)}</b></blockquote>\n<blockquote>{esc(desc)}</blockquote>\n"
    buttons = []
    idx = 0
    for key, p in db["plans"].items():
        if p.get("category") != cat:
            continue
        idx += 1
        sc = stock_count(key)
        st_badge = f"🟢 {esc(t['badge_instant'])} ({sc})" if sc > 0 else f"🟡 {esc(t['badge_fast'])}"
        text += (
            f"<blockquote><b>{esc(p['name'])}</b>\n"
            f"⚙️ <code>{esc(p['specs'])}</code>\n"
            f"⭐ <b>{p['stars']} {esc(t['lbl_stars'])}</b>  |  💰 <b>₹{p['inr']}</b>  |  📅 {p['days']} {esc(t['lbl_days'])}\n"
            f"📦 {esc(t['lbl_status'])}: {st_badge}</blockquote>\n"
        )
        style = "primary" if idx % 2 == 1 else "success"
        buttons.append([{
            "text": f"🛒 {t['btn_buy']} {p['name'][:20]} — ⭐{p['stars']} / ₹{p['inr']}",
            "callback_data": f"plan_{key}",
            "style": style,
        }])

    if not buttons:
        text += f"<blockquote>📭 {esc(t['no_plans'])}</blockquote>"

    buttons.append([{"text": t["btn_back_home"], "callback_data": "ui_home", "style": "danger"}])
    return text, buttons


async def build_plan_checkout_ui(uid: int, plan_key: str):
    t = await get_pack(get_user_lang(uid))
    p = db["plans"].get(plan_key)
    if not p:
        return "<blockquote>❌ Plan not found.</blockquote>", [[{"text": t["btn_back_home"], "callback_data": "ui_home", "style": "danger"}]]

    deliv = t["deliv_instant"] if stock_count(plan_key) > 0 else t["deliv_manual"]
    text = (
        f"<blockquote>🛒 <b>{esc(t['checkout_title'])}</b></blockquote>\n"
        f"<blockquote>"
        f"╭ 📦 <b>{esc(t['lbl_plan'])}:</b> {esc(p['name'])}\n"
        f"├ ⚙️ <b>{esc(t['lbl_specs'])}:</b> <code>{esc(p['specs'])}</code>\n"
        f"├ 📅 <b>{esc(t['lbl_validity'])}:</b> <code>{p['days']} {esc(t['lbl_days'])}</code>\n"
        f"├ 🚀 <b>{esc(t['lbl_delivery'])}:</b> <code>{esc(deliv)}</code>\n"
        f"├ ⭐ <b>{esc(t['lbl_stars_price'])}:</b> <code>{p['stars']} {esc(t['lbl_stars'])}</code>\n"
        f"╰ 💳 <b>{esc(t['lbl_upi_price'])}:</b> <code>₹{p['inr']} INR</code>"
        f"</blockquote>\n"
        f"<blockquote>👇 {esc(t['choose_pay'])}</blockquote>"
    )
    buttons = [
        [{"text": f"⭐ {p['stars']} — {t['btn_pay_stars']}", "callback_data": f"pay_stars_{plan_key}", "style": "primary"}],
        [{"text": f"💳 ₹{p['inr']} — {t['btn_pay_upi']}", "callback_data": f"pay_upi_{plan_key}", "style": "success"}],
        [{"text": t["btn_back_plans"], "callback_data": f"cat_{p['category']}", "style": "danger"}],
    ]
    return text, buttons


async def build_language_menu(uid: int, page: int = 0):
    cur_lang = get_user_lang(uid)
    t = await get_pack(cur_lang)

    items = list(WORLD_LANGUAGES.items())
    per_page = 12
    total_pages = max(1, (len(items) + per_page - 1) // per_page)
    page = max(0, min(page, total_pages - 1))
    slice_items = items[page * per_page:(page + 1) * per_page]

    text = (
        f"<blockquote>🌐 <b>{esc(t['lang_title'])}</b> ({page + 1}/{total_pages})</blockquote>\n"
        f"<blockquote>{esc(t['lang_desc'])}\n\n"
        f"✅ Current: <code>{esc(WORLD_LANGUAGES.get(cur_lang, cur_lang.upper()))}</code></blockquote>"
    )

    buttons = []
    for i in range(0, len(slice_items), 2):
        row = []
        for code, label in slice_items[i:i + 2]:
            is_cur = (code == cur_lang)
            row.append({
                "text": f"✅ {label}" if is_cur else label,
                "callback_data": f"lang_set_{code}",
                "style": "success" if is_cur else "primary",
            })
        buttons.append(row)

    nav_row = []
    if page > 0:
        nav_row.append({"text": t["btn_prev"], "callback_data": f"lang_menu_{page - 1}", "style": "primary"})
    if page < total_pages - 1:
        nav_row.append({"text": t["btn_next"], "callback_data": f"lang_menu_{page + 1}", "style": "primary"})
    if nav_row:
        buttons.append(nav_row)

    buttons.append([{"text": t["btn_lang_search"], "callback_data": "lang_search", "style": "success"}])
    buttons.append([{"text": t["btn_back_home"], "callback_data": "ui_home", "style": "danger"}])
    return text, buttons


def build_admin_ui():
    total_users = len(db["users"])
    completed = [o for o in db["orders"].values() if o["status"] == "completed"]
    pending = [o for o in db["orders"].values() if o["status"] in ("pending_approval", "paid_waiting_delivery")]
    inr_rev = sum(o["amount"] for o in completed if o["currency"] == "INR")
    stars_rev = sum(o["amount"] for o in completed if o["currency"] == "XTR")
    total_stock = sum(len(v) for v in db["stock"].values())

    text = (
        f"<blockquote>👑 <b>OWNER ADMIN DASHBOARD</b></blockquote>\n"
        f"<blockquote>"
        f"╭ 👥 <b>Total Users:</b> <code>{total_users}</code>\n"
        f"├ ✅ <b>Completed Orders:</b> <code>{len(completed)}</code>\n"
        f"├ ⏳ <b>Pending Orders:</b> <code>{len(pending)}</code>\n"
        f"├ 💰 <b>UPI Revenue:</b> <code>₹{inr_rev}</code>\n"
        f"├ ⭐ <b>Stars Revenue:</b> <code>{stars_rev} Stars</code>\n"
        f"├ 📦 <b>Loaded Stock:</b> <code>{total_stock} Ready</code>\n"
        f"╰ 🏦 <b>UPI ID:</b> <code>{esc(db['settings']['upi_id'])}</code>"
        f"</blockquote>\n"
        f"<blockquote><b>⚡ Admin Commands:</b>\n"
        f"• <code>/deliver ORDER_ID Details...</code>\n"
        f"• <code>/addstock PLAN_KEY Details...</code>\n"
        f"• <code>/setprice PLAN_KEY INR STARS</code>\n"
        f"• <code>/setupi yourupi@fam</code> | <code>/setqr</code> (reply to QR photo)\n"
        f"• <code>/broadcast</code> (reply to any message)\n"
        f"• <code>/backup</code> | <code>/restore</code> (reply to .json file)</blockquote>"
    )
    buttons = [
        [
            {"text": f"⏳ Pending Orders ({len(pending)})", "callback_data": "adm_pending", "style": "danger"},
            {"text": f"📦 Stock Status ({total_stock})", "callback_data": "adm_stock", "style": "primary"},
        ],
        [
            {"text": "💾 Send DB Backup", "callback_data": "adm_backup", "style": "success"},
            {"text": "🔄 Refresh", "callback_data": "adm_home", "style": "primary"},
        ],
        [{"text": "🔙 Back to Store Menu", "callback_data": "ui_home", "style": "danger"}],
    ]
    return text, buttons


# =============================================================================
# 7. ORDER FULFILLMENT ENGINE (AUTO-STOCK + MANUAL DELIVERY)
# =============================================================================
async def deliver_order(order_id: str, credentials: str) -> bool:
    order = db["orders"].get(order_id)
    if not order:
        return False
    plan = db["plans"].get(order["plan_key"], {"days": 30, "name": order["plan_name"]})
    days = int(plan.get("days", 30))
    now = time.time()

    order["status"] = "completed"
    order["credentials"] = credentials
    order["delivered_at"] = now
    order["expires_at"] = now + (days * 86400)
    order["reminded_3d"] = False
    order["reminded_exp"] = False
    save_db()

    t = await get_pack(get_user_lang(order["user_id"]))
    user_text = (
        f"<blockquote>🎉 <b>{esc(t['server_ready_title'])}!</b></blockquote>\n"
        f"<blockquote>"
        f"╭ 🆔 <b>{esc(t['lbl_order_id'])}:</b> <code>{esc(order_id)}</code>\n"
        f"├ 📦 <b>{esc(t['lbl_plan'])}:</b> {esc(order['plan_name'])}\n"
        f"╰ 📅 <b>{esc(t['valid_till'])}:</b> <code>{fmt_date(order['expires_at'])} ({days} {esc(t['lbl_days'])})</code>"
        f"</blockquote>\n"
        f"<blockquote>🔐 <b>{esc(t['lbl_login_details'])}:</b>\n"
        f"<code>{esc(credentials)}</code></blockquote>\n"
        f"<blockquote>⚠️ {esc(t['rule_note'])}</blockquote>"
    )
    await send_msg(
        order["user_id"],
        user_text,
        buttons=[
            [{"text": t["btn_services"], "callback_data": "my_services", "style": "success"}],
            [{"text": t["btn_support"], "url": f"https://t.me/{db['settings']['support'].lstrip('@')}", "style": "primary"}],
        ],
    )
    return True


async def handle_paid_order_fulfillment(order_id: str):
    order = db["orders"].get(order_id)
    if not order:
        return

    plan_key = order["plan_key"]
    stock_list = db["stock"].get(plan_key, [])

    if stock_list:
        creds = stock_list.pop(0)
        db["stock"][plan_key] = stock_list
        save_db()
        await deliver_order(order_id, creds)
        await send_msg(
            OWNER_ID,
            f"<blockquote>⚡ <b>AUTO-DELIVERED FROM STOCK!</b></blockquote>\n"
            f"<blockquote>🆔 <b>Order:</b> <code>{esc(order_id)}</code>\n"
            f"👤 <b>Buyer:</b> {esc(order['user_name'])} (<code>{order['user_id']}</code>)\n"
            f"📦 <b>Plan:</b> {esc(order['plan_name'])}\n"
            f"💰 <b>Paid:</b> <code>{order['amount']} {order['currency']}</code>\n"
            f"📊 <b>Remaining Stock:</b> <code>{len(stock_list)}</code></blockquote>",
        )
    else:
        order["status"] = "paid_waiting_delivery"
        save_db()
        t = await get_pack(get_user_lang(order["user_id"]))
        await send_msg(
            order["user_id"],
            f"<blockquote>✅ <b>{esc(t['pay_confirmed_title'])}!</b></blockquote>\n"
            f"<blockquote>🆔 <b>{esc(t['lbl_order_id'])}:</b> <code>{esc(order_id)}</code>\n"
            f"📦 <b>{esc(t['lbl_plan'])}:</b> {esc(order['plan_name'])}\n"
            f"⏳ {esc(t['pay_confirmed_desc'])}</blockquote>",
            buttons=[[{"text": t["btn_orders"], "callback_data": "my_orders", "style": "primary"}]],
        )
        await send_msg(
            OWNER_ID,
            f"<blockquote>🔔 <b>NEW PAID ORDER — MANUAL DELIVERY NEEDED</b></blockquote>\n"
            f"<blockquote>🆔 <b>Order ID:</b> <code>{esc(order_id)}</code>\n"
            f"👤 <b>Buyer:</b> {esc(order['user_name'])} (<code>{order['user_id']}</code>)\n"
            f"📦 <b>Plan:</b> {esc(order['plan_name'])}\n"
            f"💰 <b>Paid:</b> <code>{order['amount']} {order['currency']}</code> ({order['method'].upper()})</blockquote>\n"
            f"<blockquote>👇 Send credentials using this command:\n"
            f"<code>/deliver {esc(order_id)} IP/URL: ... User: ... Pass: ...</code></blockquote>",
        )


# =============================================================================
# 8. UPDATE ROUTERS (MESSAGES, CALLBACKS, STARS PAYMENTS)
# =============================================================================
async def handle_pre_checkout(query: dict):
    qid = query["id"]
    order_id = query.get("invoice_payload", "")
    if order_id in db["orders"]:
        await tg_call("answerPreCheckoutQuery", {"pre_checkout_query_id": qid, "ok": True})
    else:
        await tg_call("answerPreCheckoutQuery", {
            "pre_checkout_query_id": qid,
            "ok": False,
            "error_message": "Order expired! Please select the plan again.",
        })


async def handle_successful_payment(msg: dict):
    user = msg.get("from", {})
    register_user(user)
    sp = msg["successful_payment"]
    order_id = sp.get("invoice_payload", "")
    order = db["orders"].get(order_id)

    if not order:
        order_id = f"STR{uuid.uuid4().hex[:6].upper()}"
        db["orders"][order_id] = {
            "id": order_id,
            "user_id": user["id"],
            "user_name": user.get("first_name", "User"),
            "plan_key": "custom",
            "plan_name": "Telegram Stars Order",
            "method": "stars",
            "amount": sp.get("total_amount", 0),
            "currency": sp.get("currency", "XTR"),
            "status": "paid_waiting_delivery",
            "created_at": time.time(),
            "charge_id": sp.get("telegram_payment_charge_id", ""),
        }
        save_db()
    else:
        order["charge_id"] = sp.get("telegram_payment_charge_id", "")
        order["amount"] = sp.get("total_amount", order["amount"])
        save_db()

    await handle_paid_order_fulfillment(order_id)


async def handle_callback(cb: dict):
    cb_id = cb["id"]
    user = cb.get("from", {})
    uid = user["id"]
    register_user(user)
    msg = cb.get("message", {})
    chat_id = msg.get("chat", {}).get("id", uid)
    msg_id = msg.get("message_id")
    is_photo_msg = bool(msg.get("photo"))
    data = cb.get("data", "")

    async def _show(text: str, buttons: list):
        if is_photo_msg:
            await delete_msg(chat_id, msg_id)
            await send_msg(chat_id, text, buttons)
        else:
            await edit_msg(chat_id, msg_id, text, buttons)

    if data == "ui_home":
        pending_upi_proof.pop(str(uid), None)
        await_lang_input.discard(str(uid))
        txt, btns = await build_home_ui(uid, user.get("first_name", "User"))
        await _show(txt, btns)
        return await answer_cb(cb_id)

    if data.startswith("lang_menu_"):
        await_lang_input.discard(str(uid))
        page = int(data.split("_")[-1]) if data.split("_")[-1].isdigit() else 0
        txt, btns = await build_language_menu(uid, page)
        await _show(txt, btns)
        return await answer_cb(cb_id)

    if data == "lang_search":
        await_lang_input.add(str(uid))
        t = await get_pack(get_user_lang(uid))
        await _show(
            f"<blockquote>🔎 <b>{esc(t['btn_lang_search'])}</b></blockquote>\n"
            f"<blockquote>{esc(t['lang_search_prompt'])}</blockquote>",
            [[{"text": t["btn_back_home"], "callback_data": "ui_home", "style": "danger"}]],
        )
        return await answer_cb(cb_id)

    if data.startswith("lang_set_"):
        code = data.split("lang_set_", 1)[1]
        await answer_cb(cb_id, "⏳ Loading language...")
        await get_pack(code)
        set_user_lang(uid, code)
        await_lang_input.discard(str(uid))
        txt, btns = await build_home_ui(uid, user.get("first_name", "User"))
        await _show(txt, btns)
        return

    if data.startswith("cat_"):
        cat = data.split("_", 1)[1]
        txt, btns = await build_category_ui(uid, cat)
        await _show(txt, btns)
        return await answer_cb(cb_id)

    if data.startswith("plan_"):
        plan_key = data.split("_", 1)[1]
        txt, btns = await build_plan_checkout_ui(uid, plan_key)
        await _show(txt, btns)
        return await answer_cb(cb_id)

    if data.startswith("pay_stars_"):
        plan_key = data.split("pay_stars_", 1)[1]
        p = db["plans"].get(plan_key)
        if not p:
            return await answer_cb(cb_id, "❌ Plan not found!", alert=True)

        order_id = f"STR{uuid.uuid4().hex[:6].upper()}"
        db["orders"][order_id] = {
            "id": order_id,
            "user_id": uid,
            "user_name": user.get("first_name", "User"),
            "plan_key": plan_key,
            "plan_name": p["name"],
            "method": "stars",
            "amount": int(p["stars"]),
            "currency": "XTR",
            "status": "pending_stars",
            "created_at": time.time(),
        }
        save_db()

        res = await send_stars_invoice(chat_id, p, order_id)
        if res.get("ok"):
            await answer_cb(cb_id, "⭐ Telegram Stars invoice sent!")
        else:
            await answer_cb(cb_id, f"❌ Invoice Error: {res.get('description', 'Try again')[:80]}", alert=True)
        return

    if data.startswith("pay_upi_"):
        plan_key = data.split("pay_upi_", 1)[1]
        p = db["plans"].get(plan_key)
        if not p:
            return await answer_cb(cb_id, "❌ Plan not found!", alert=True)

        order_id = f"UPI{uuid.uuid4().hex[:6].upper()}"
        db["orders"][order_id] = {
            "id": order_id,
            "user_id": uid,
            "user_name": user.get("first_name", "User"),
            "plan_key": plan_key,
            "plan_name": p["name"],
            "method": "upi",
            "amount": int(p["inr"]),
            "currency": "INR",
            "status": "pending_proof",
            "created_at": time.time(),
        }
        pending_upi_proof[str(uid)] = order_id
        save_db()

        t = await get_pack(get_user_lang(uid))
        upi_id = db["settings"]["upi_id"]
        qr_fid = db["settings"].get("qr_file_id", "")
        txt = (
            f"<blockquote>💳 <b>{esc(t['upi_title'])} — {esc(order_id)}</b></blockquote>\n"
            f"<blockquote>"
            f"╭ 📦 <b>{esc(t['lbl_plan'])}:</b> {esc(p['name'])}\n"
            f"├ 💰 <b>{esc(t['lbl_exact_amt'])}:</b> <code>₹{p['inr']} INR</code>\n"
            f"╰ 🏦 <b>{esc(t['lbl_upi_id'])}:</b> <code>{esc(upi_id)}</code>"
            f"</blockquote>\n"
            f"<blockquote>📸 {esc(t['upi_next_step'])}</blockquote>"
        )
        btns = [[{"text": t["btn_cancel_pay"], "callback_data": "ui_home", "style": "danger"}]]
        if qr_fid:
            await delete_msg(chat_id, msg_id)
            await send_photo(chat_id, qr_fid, txt, btns)
        else:
            await _show(txt, btns)
        return await answer_cb(cb_id, "💳 UPI payment details ready!")

    if data == "my_services":
        t = await get_pack(get_user_lang(uid))
        active = [o for o in db["orders"].values() if o["user_id"] == uid and o["status"] == "completed"]
        if not active:
            txt = f"<blockquote>📭 {esc(t['no_services'])}</blockquote>"
        else:
            blocks = [f"<blockquote>📦 <b>{esc(t['my_services_title'])}</b></blockquote>"]
            for o in active[-5:]:
                dl = days_left(o.get("expires_at", 0))
                badge = f"🟢 {dl} {esc(t['days_left'])}" if dl > 0 else f"🔴 {esc(t['expired'])}"
                blocks.append(
                    f"<blockquote><b>{esc(o['plan_name'])}</b> ({badge})\n"
                    f"🆔 <code>{esc(o['id'])}</code> | 📅 {esc(t['valid_till'])}: <code>{fmt_date(o.get('expires_at', 0))}</code>\n"
                    f"🔐 <code>{esc(o.get('credentials', 'N/A'))}</code></blockquote>"
                )
            txt = "\n".join(blocks)
        await _show(txt, [[{"text": t["btn_back_home"], "callback_data": "ui_home", "style": "danger"}]])
        return await answer_cb(cb_id)

    if data == "my_orders":
        t = await get_pack(get_user_lang(uid))
        my_o = [o for o in db["orders"].values() if o["user_id"] == uid]
        if not my_o:
            txt = f"<blockquote>🧾 {esc(t['no_orders'])}</blockquote>"
        else:
            blocks = [f"<blockquote>🧾 <b>{esc(t['my_orders_title'])}</b></blockquote>"]
            for o in my_o[-8:][::-1]:
                sym = "₹" if o["currency"] == "INR" else "⭐"
                blocks.append(
                    f"<blockquote>🆔 <code>{esc(o['id'])}</code> — {esc(o['plan_name'])}\n"
                    f"💰 <code>{sym}{o['amount']}</code> | {esc(t['lbl_status'])}: <code>{esc(o['status'])}</code></blockquote>"
                )
            txt = "\n".join(blocks)
        await _show(txt, [[{"text": t["btn_back_home"], "callback_data": "ui_home", "style": "danger"}]])
        return await answer_cb(cb_id)

    if data == "show_rules":
        t = await get_pack(get_user_lang(uid))
        txt = (
            f"<blockquote>📜 <b>{esc(STORE_NAME.upper())} — {esc(t['rules_title'])}</b></blockquote>\n"
            f"<blockquote>"
            f"1️⃣ {esc(t['rule_1'])}\n\n"
            f"2️⃣ {esc(t['rule_2'])}\n\n"
            f"3️⃣ {esc(t['rule_3'])}\n\n"
            f"4️⃣ {esc(t['rule_4'])}"
            f"</blockquote>"
        )
        await _show(txt, [[{"text": t["btn_back_home"], "callback_data": "ui_home", "style": "danger"}]])
        return await answer_cb(cb_id)

    # ---------------- OWNER ADMIN CALLBACKS ----------------
    if not is_owner(uid):
        return await answer_cb(cb_id, "🔒 Owner only!", alert=True)

    if data == "adm_home":
        txt, btns = build_admin_ui()
        await _show(txt, btns)
        return await answer_cb(cb_id)

    if data == "adm_pending":
        pend = [o for o in db["orders"].values() if o["status"] in ("pending_approval", "paid_waiting_delivery")]
        if not pend:
            txt = "<blockquote>✅ No pending orders right now!</blockquote>"
        else:
            blocks = [f"<blockquote>⏳ <b>PENDING ORDERS ({len(pend)})</b></blockquote>"]
            for o in pend[-10:]:
                blocks.append(
                    f"<blockquote>🆔 <code>{esc(o['id'])}</code> | {esc(o['plan_name'])}\n"
                    f"👤 {esc(o['user_name'])} (<code>{o['user_id']}</code>)\n"
                    f"💰 <code>{o['amount']} {o['currency']}</code> | <code>{o['status']}</code>\n"
                    f"📤 <code>/deliver {esc(o['id'])} DETAILS</code></blockquote>"
                )
            txt = "\n".join(blocks)
        await _show(txt, [[{"text": "🔙 Admin Dashboard", "callback_data": "adm_home", "style": "danger"}]])
        return await answer_cb(cb_id)

    if data == "adm_stock":
        blocks = ["<blockquote>📦 <b>LOADED AUTO-DELIVERY STOCK</b></blockquote>"]
        for k, p in db["plans"].items():
            blocks.append(f"<blockquote>• <code>{esc(k)}</code> ({esc(p['name'])}): <b>{stock_count(k)}</b> Ready</blockquote>")
        blocks.append("<blockquote>➕ Add stock using:\n<code>/addstock panel_1gb Panel: https://... User: ... Pass: ...</code></blockquote>")
        await _show("\n".join(blocks), [[{"text": "🔙 Admin Dashboard", "callback_data": "adm_home", "style": "danger"}]])
        return await answer_cb(cb_id)

    if data == "adm_backup":
        await send_db_backup(uid, f"💾 <b>{esc(STORE_NAME)} DB Backup</b> — {fmt_date(time.time())}")
        return await answer_cb(cb_id, "✅ Backup sent!", alert=True)

    if data.startswith("adm_approve_"):
        oid = data.split("adm_approve_", 1)[1]
        order = db["orders"].get(oid)
        if not order:
            return await answer_cb(cb_id, "❌ Order not found!", alert=True)
        if order["status"] == "completed":
            return await answer_cb(cb_id, "✅ Already delivered!", alert=True)
        await handle_paid_order_fulfillment(oid)
        return await answer_cb(cb_id, "✅ Payment Approved!", alert=True)

    if data.startswith("adm_reject_"):
        oid = data.split("adm_reject_", 1)[1]
        order = db["orders"].get(oid)
        if not order:
            return await answer_cb(cb_id, "❌ Order not found!", alert=True)
        order["status"] = "rejected"
        save_db()
        t = await get_pack(get_user_lang(order["user_id"]))
        await send_msg(
            order["user_id"],
            f"<blockquote>❌ <b>{esc(t['pay_rejected_title'])}</b></blockquote>\n"
            f"<blockquote>🆔 <b>{esc(t['lbl_order_id'])}:</b> <code>{esc(oid)}</code>\n"
            f"{esc(t['pay_rejected_desc'])}</blockquote>",
            buttons=[[{"text": t["btn_support"], "url": f"https://t.me/{db['settings']['support'].lstrip('@')}", "style": "danger"}]],
        )
        await send_msg(OWNER_ID, f"<blockquote>🗑 Order <code>{esc(oid)}</code> marked as Rejected.</blockquote>")
        return await answer_cb(cb_id, "❌ Order Rejected!", alert=True)

    await answer_cb(cb_id)


async def handle_message(msg: dict):
    if "successful_payment" in msg:
        return await handle_successful_payment(msg)

    chat = msg.get("chat", {})
    if chat.get("type") != "private":
        return

    user = msg.get("from", {})
    uid = user.get("id")
    if not uid:
        return
    register_user(user)

    text = (msg.get("text") or "").strip()
    caption = (msg.get("caption") or "").strip()
    photos = msg.get("photo")
    reply = msg.get("reply_to_message")
    msg_id = msg.get("message_id")

    # 1. Handle UPI Payment Screenshot Upload from User
    if photos and str(uid) in pending_upi_proof and not text.startswith("/"):
        oid = pending_upi_proof.pop(str(uid))
        order = db["orders"].get(oid)
        if order:
            file_id = photos[-1]["file_id"]
            order["status"] = "pending_approval"
            order["proof_file_id"] = file_id
            order["utr_note"] = caption or "No note"
            save_db()

            t = await get_pack(get_user_lang(uid))
            await send_msg(
                uid,
                f"<blockquote>✅ <b>{esc(t['ss_received_title'])}!</b></blockquote>\n"
                f"<blockquote>🆔 <b>{esc(t['lbl_order_id'])}:</b> <code>{esc(oid)}</code>\n"
                f"📦 <b>{esc(t['lbl_plan'])}:</b> {esc(order['plan_name'])}\n"
                f"⏳ {esc(t['ss_received_desc'])}</blockquote>",
                buttons=[[{"text": t["btn_back_home"], "callback_data": "ui_home", "style": "primary"}]],
                reply_to=msg_id,
            )

            st_avail = stock_count(order["plan_key"])
            adm_cap = (
                f"<blockquote>💳 <b>NEW UPI PAYMENT PROOF</b></blockquote>\n"
                f"<blockquote>"
                f"╭ 🆔 <b>Order:</b> <code>{esc(oid)}</code>\n"
                f"├ 👤 <b>User:</b> {esc(user.get('first_name', 'User'))} (<code>{uid}</code>)\n"
                f"├ 📦 <b>Plan:</b> {esc(order['plan_name'])}\n"
                f"├ 💰 <b>Amount:</b> <code>₹{order['amount']}</code>\n"
                f"├ 📝 <b>UTR/Note:</b> <code>{esc(order['utr_note'])}</code>\n"
                f"╰ 📊 <b>Stock Ready:</b> <code>{st_avail}</code>"
                f"</blockquote>"
            )
            approve_label = "⚡ Approve & Auto-Deliver" if st_avail > 0 else "✅ Approve Payment"
            adm_btns = [[
                {"text": approve_label, "callback_data": f"adm_approve_{oid}", "style": "success"},
                {"text": "❌ Reject", "callback_data": f"adm_reject_{oid}", "style": "danger"},
            ]]
            await send_photo(OWNER_ID, file_id, adm_cap, adm_btns)
            return

    if not text:
        return

    # 2. Handle Custom Language Search Input
    if str(uid) in await_lang_input and not text.startswith("/"):
        code = resolve_language_query(text)
        if not code:
            t = await get_pack(get_user_lang(uid))
            return await send_msg(uid, f"<blockquote>❌ {esc(t['lang_not_found'])}</blockquote>", reply_to=msg_id)
        await_lang_input.discard(str(uid))
        await get_pack(code)
        set_user_lang(uid, code)
        txt, btns = await build_home_ui(uid, user.get("first_name", "User"))
        return await send_msg(uid, txt, btns, reply_to=msg_id)

    parts = text.split()
    cmd = parts[0].lower().split("@")[0]

    # 3. User Commands
    if cmd == "/start":
        pending_upi_proof.pop(str(uid), None)
        await_lang_input.discard(str(uid))
        txt, btns = await build_home_ui(uid, user.get("first_name", "User"))
        return await send_msg(uid, txt, btns, reply_to=msg_id)

    if cmd in ("/lang", "/language"):
        if len(parts) >= 2:
            code = resolve_language_query(" ".join(parts[1:]))
            if code:
                await get_pack(code)
                set_user_lang(uid, code)
                txt, btns = await build_home_ui(uid, user.get("first_name", "User"))
                return await send_msg(uid, txt, btns, reply_to=msg_id)
        txt, btns = await build_language_menu(uid, 0)
        return await send_msg(uid, txt, btns, reply_to=msg_id)

    # 4. Owner Admin Commands (Always English)
    if not is_owner(uid):
        return

    if cmd == "/admin":
        txt, btns = build_admin_ui()
        return await send_msg(uid, txt, btns, reply_to=msg_id)

    if cmd == "/deliver":
        sp = text.split(None, 2)
        if len(sp) < 3:
            return await send_msg(
                uid,
                "<blockquote>⚠️ Usage: <code>/deliver ORDER_ID IP: ... User: ... Pass: ...</code></blockquote>",
                reply_to=msg_id,
            )
        oid, creds = sp[1].strip(), sp[2].strip()
        if await deliver_order(oid, creds):
            return await send_msg(uid, f"<blockquote>✅ Order <code>{esc(oid)}</code> delivered to the customer!</blockquote>", reply_to=msg_id)
        return await send_msg(uid, f"<blockquote>❌ Order ID <code>{esc(oid)}</code> not found.</blockquote>", reply_to=msg_id)

    if cmd == "/addstock":
        sp = text.split(None, 2)
        if len(sp) < 3 or sp[1] not in db["plans"]:
            keys = ", ".join(f"<code>{k}</code>" for k in db["plans"])
            return await send_msg(
                uid,
                f"<blockquote>⚠️ Usage: <code>/addstock PLAN_KEY Credentials...</code>\nAvailable Keys: {keys}</blockquote>",
                reply_to=msg_id,
            )
        pkey, creds = sp[1].strip(), sp[2].strip()
        db["stock"].setdefault(pkey, []).append(creds)
        save_db()
        return await send_msg(
            uid,
            f"<blockquote>✅ Stock added to <code>{esc(pkey)}</code>! Total ready: <code>{stock_count(pkey)}</code></blockquote>",
            reply_to=msg_id,
        )

    if cmd == "/setprice":
        if len(parts) < 4 or not parts[2].isdigit() or not parts[3].isdigit():
            keys = ", ".join(f"<code>{k}</code>" for k in db["plans"])
            return await send_msg(
                uid,
                f"<blockquote>⚠️ Usage: <code>/setprice PLAN_KEY INR STARS</code>\nExample: <code>/setprice panel_1gb 100 75</code>\nKeys: {keys}</blockquote>",
                reply_to=msg_id,
            )
        pkey = parts[1].strip()
        if pkey not in db["plans"]:
            return await send_msg(uid, f"<blockquote>❌ Invalid plan key: <code>{esc(pkey)}</code></blockquote>", reply_to=msg_id)
        db["plans"][pkey]["inr"] = int(parts[2])
        db["plans"][pkey]["stars"] = int(parts[3])
        save_db()
        return await send_msg(
            uid,
            f"<blockquote>✅ Price updated for <code>{esc(pkey)}</code>: <b>₹{parts[2]}</b> | ⭐ <b>{parts[3]} Stars</b></blockquote>",
            reply_to=msg_id,
        )

    if cmd == "/setupi":
        if len(parts) < 2:
            return await send_msg(uid, "<blockquote>⚠️ Usage: <code>/setupi yourupi@fam</code></blockquote>", reply_to=msg_id)
        db["settings"]["upi_id"] = parts[1].strip()
        save_db()
        return await send_msg(uid, f"<blockquote>✅ UPI ID updated to: <code>{esc(parts[1].strip())}</code></blockquote>", reply_to=msg_id)

    if cmd == "/setqr":
        if not reply or not reply.get("photo"):
            return await send_msg(uid, "<blockquote>⚠️ Reply to your UPI QR code photo with <code>/setqr</code>.</blockquote>", reply_to=msg_id)
        db["settings"]["qr_file_id"] = reply["photo"][-1]["file_id"]
        save_db()
        return await send_msg(uid, "<blockquote>✅ UPI QR Code saved! Customers will see this QR on UPI checkout.</blockquote>", reply_to=msg_id)

    if cmd == "/broadcast":
        if not reply:
            return await send_msg(uid, "<blockquote>⚠️ Reply to any message with <code>/broadcast</code>.</blockquote>", reply_to=msg_id)
        sent, failed = 0, 0
        for u in list(db["users"].keys()):
            res = await tg_call("copyMessage", {
                "chat_id": int(u),
                "from_chat_id": uid,
                "message_id": reply["message_id"],
            })
            if res.get("ok"):
                sent += 1
            else:
                failed += 1
            await asyncio.sleep(0.05)
        return await send_msg(uid, f"<blockquote>📢 <b>Broadcast Complete!</b>\n✅ Sent: <code>{sent}</code> | ❌ Failed: <code>{failed}</code></blockquote>", reply_to=msg_id)

    if cmd == "/backup":
        target = BACKUP_CHANNEL or uid
        await send_db_backup(target, f"💾 <b>{esc(STORE_NAME)} DB Backup</b> — {fmt_date(time.time())}")
        if target != uid:
            await send_msg(uid, "<blockquote>✅ Backup sent to Backup Channel!</blockquote>", reply_to=msg_id)
        return

    if cmd == "/restore":
        if not reply or not reply.get("document"):
            return await send_msg(uid, "<blockquote>⚠️ Reply to your backup <code>store_db.json</code> file with <code>/restore</code>.</blockquote>", reply_to=msg_id)
        fid = reply["document"]["file_id"]
        finfo = await tg_call("getFile", {"file_id": fid})
        if not finfo.get("ok"):
            return await send_msg(uid, "<blockquote>❌ File download failed.</blockquote>", reply_to=msg_id)
        fpath = finfo["result"]["file_path"]
        dl_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{fpath}"
        async with http_session.get(dl_url) as r:
            raw = await r.read()
        try:
            loaded = json.loads(raw.decode("utf-8"))
            for k in ("users", "plans", "stock", "orders", "settings"):
                if k in loaded:
                    db[k] = loaded[k]
            save_db()
            return await send_msg(
                uid,
                f"<blockquote>♻️ <b>DATABASE RESTORED!</b>\n👥 Users: <code>{len(db['users'])}</code> | 🧾 Orders: <code>{len(db['orders'])}</code></blockquote>",
                reply_to=msg_id,
            )
        except Exception as e:
            return await send_msg(uid, f"<blockquote>❌ Invalid JSON file: <code>{esc(e)}</code></blockquote>", reply_to=msg_id)


# =============================================================================
# 9. EXPIRY WATCHER & MAIN LONG-POLLING LOOP
# =============================================================================
async def expiry_watcher():
    while not _shutdown:
        try:
            now = time.time()
            changed = False
            for oid, o in list(db["orders"].items()):
                if o.get("status") != "completed" or not o.get("expires_at"):
                    continue
                rem = o["expires_at"] - now
                if 0 < rem <= 3 * 86400 and not o.get("reminded_3d"):
                    o["reminded_3d"] = True
                    changed = True
                    t = await get_pack(get_user_lang(o["user_id"]))
                    await send_msg(
                        o["user_id"],
                        f"<blockquote>⏰ <b>{esc(t['renew_title'])}</b></blockquote>\n"
                        f"<blockquote>📦 <b>{esc(t['lbl_plan'])}:</b> {esc(o['plan_name'])}\n"
                        f"🆔 <b>{esc(t['lbl_order_id'])}:</b> <code>{esc(oid)}</code>\n"
                        f"⏳ <code>{days_left(o['expires_at'])} {esc(t['days_left'])}</code>\n"
                        f"{esc(t['renew_desc'])}</blockquote>",
                        buttons=[[{"text": t["btn_renew"], "callback_data": f"plan_{o['plan_key']}", "style": "success"}]],
                    )
                elif rem <= 0 and not o.get("reminded_exp"):
                    o["reminded_exp"] = True
                    o["status"] = "expired"
                    changed = True
                    t = await get_pack(get_user_lang(o["user_id"]))
                    await send_msg(
                        o["user_id"],
                        f"<blockquote>🔴 <b>{esc(t['expired_title'])}</b></blockquote>\n"
                        f"<blockquote>📦 {esc(o['plan_name'])} (<code>{esc(oid)}</code>)\n"
                        f"{esc(t['expired_desc'])}</blockquote>",
                        buttons=[[{"text": t["btn_order_again"], "callback_data": "ui_home", "style": "primary"}]],
                    )
                    await send_msg(
                        OWNER_ID,
                        f"<blockquote>🔴 <b>CLIENT SERVER EXPIRED</b></blockquote>\n"
                        f"<blockquote>👤 {esc(o['user_name'])} (<code>{o['user_id']}</code>)\n"
                        f"📦 {esc(o['plan_name'])} | 🆔 <code>{esc(oid)}</code>\n"
                        f"You can now suspend/stop this user's server or panel.</blockquote>",
                    )
            if changed:
                save_db()
        except Exception as e:
            print(f"[Expiry Watcher Warning] {e}")
        await asyncio.sleep(1800)


async def poll_updates():
    offset = 0
    await tg_call("deleteWebhook", {"drop_pending_updates": False})
    await tg_call("setMyCommands", {
        "commands": [
            {"command": "start", "description": "⚡ Open VPS & Bot Hosting Store"},
            {"command": "lang", "description": "🌐 Change Language (100+ Languages)"},
            {"command": "admin", "description": "👑 Owner Admin Dashboard"},
        ]
    })
    me = await tg_call("getMe")
    uname = me.get("result", {}).get("username", "Bot")
    print(f"🚀 {STORE_NAME} Started as @{uname}")

    while not _shutdown:
        try:
            res = await tg_call("getUpdates", {
                "offset": offset,
                "timeout": 30,
                "allowed_updates": ["message", "callback_query", "pre_checkout_query"],
            })
            if res.get("ok"):
                for upd in res.get("result", []):
                    offset = upd["update_id"] + 1
                    try:
                        if "pre_checkout_query" in upd:
                            asyncio.create_task(handle_pre_checkout(upd["pre_checkout_query"]))
                        elif "callback_query" in upd:
                            asyncio.create_task(handle_callback(upd["callback_query"]))
                        elif "message" in upd:
                            asyncio.create_task(handle_message(upd["message"]))
                    except Exception as ie:
                        print(f"[Update Error] {ie}")
            else:
                await asyncio.sleep(3)
        except Exception as e:
            print(f"[Polling Warning] {e}")
            await asyncio.sleep(3)


async def main():
    global http_session
    if not BOT_TOKEN or not OWNER_ID:
        print("❌ BOT_TOKEN and OWNER_ID must be set in Environment / .env!")
        return

    load_db()
    http_session = aiohttp.ClientSession()
    web_runner = await start_web_server()
    watcher_task = asyncio.create_task(expiry_watcher())

    try:
        await poll_updates()
    finally:
        watcher_task.cancel()
        await web_runner.cleanup()
        await http_session.close()


if __name__ == "__main__":
    asyncio.run(main())
