import os
from dotenv import load_dotenv

load_dotenv(".env")

MAX_BOT = int(os.getenv("MAX_BOT", "9999"))

DEVS = list(map(int, os.getenv("DEVS", "1311431740").split()))

API_ID = int(os.getenv("API_ID", "38773229"))

API_HASH = os.getenv("API_HASH", "e1885e331667b7e028d7970862aa9594")

BOT_TOKEN = os.getenv("BOT_TOKEN", "8175607450:AAEqQQ5pSeK-B7g0QRTYqwfA1kbYsvRyAeE")

OWNER_ID = int(os.getenv("OWNER_ID", "1311431740"))

BLACKLIST_CHAT = list(map(int, os.getenv("BLACKLIST_CHAT", "").split()))

RMBG_API = os.getenv("RMBG_API", "a6qxsmMJ3CsNo7HyxuKGsP1o")

MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://dwiputrasiswantofahrel_db_user:7s4Xzy6GwzscxNSD@cluster0.j1fmojl.mongodb.net/?appName=Cluster0")

LOGS_MAKER_UBOT = int(os.getenv("LOGS_MAKER_UBOT", "-1003841423220"))

PAKASIR_API_KEY = os.getenv("PAKASIR_API_KEY", "")

PAKASIR_MERCHANT_ID = os.getenv("PAKASIR_MERCHANT_ID", "")
