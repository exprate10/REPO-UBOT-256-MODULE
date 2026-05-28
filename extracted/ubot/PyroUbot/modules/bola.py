import random
from PyroUbot import *
from pyrogram import *
from pyrogram.types import *

__MODULE__ = "⚽ Tebak Bola"
__HELP__ = """
<blockquote><b>『 TEBak PEMAIN BOLA 』</b>

<b>Perintah:</b>
• <code>.bola</code> → mulai game
• <code>.jawab</code> [nama] → jawab
• <code>.bolaskor</code> → lihat skor

<b>Catatan:</b>
• Bisa semua prefix
• Main rame di grup
</blockquote>
"""

# ================= DATA PEMAIN =================

PLAYERS = [
    {"nama": "lionel messi", "clue": "🇦🇷 Argentina | Inter Miami | Forward"},
    {"nama": "cristiano ronaldo", "clue": "🇵🇹 Portugal | Al Nassr | Forward"},
    {"nama": "kylian mbappe", "clue": "🇫🇷 Prancis | PSG | Forward"},
    {"nama": "erling haaland", "clue": "🇳🇴 Norwegia | Man City | Striker"},
    {"nama": "neymar", "clue": "🇧🇷 Brasil | Al Hilal | Winger"},
    {"nama": "kevin de bruyne", "clue": "🇧🇪 Belgia | Man City | Midfielder"},
    {"nama": "luka modric", "clue": "🇭🇷 Kroasia | Real Madrid | Midfielder"},
    {"nama": "toni kroos", "clue": "🇩🇪 Jerman | Real Madrid | Midfielder"},
    {"nama": "vinicius junior", "clue": "🇧🇷 Brasil | Real Madrid | Winger"},
    {"nama": "jude bellingham", "clue": "🇬🇧 Inggris | Real Madrid | Midfielder"},
    {"nama": "mohamed salah", "clue": "🇪🇬 Mesir | Liverpool | Winger"},
    {"nama": "virgil van dijk", "clue": "🇳🇱 Belanda | Liverpool | Defender"},
    {"nama": "manuel neuer", "clue": "🇩🇪 Jerman | Bayern | GK"},
    {"nama": "harry kane", "clue": "🇬🇧 Inggris | Bayern | Striker"},
    {"nama": "son heung min", "clue": "🇰🇷 Korea | Tottenham | Forward"},
    {"nama": "ronaldinho", "clue": "🇧🇷 Brasil | Barcelona | Legend"},
    {"nama": "kaka", "clue": "🇧🇷 Brasil | AC Milan | Legend"},
    {"nama": "zlatan ibrahimovic", "clue": "🇸🇪 Swedia | AC Milan | Legend"},
]

# ================= STORAGE =================

GAME = {}
SCORE = {}

# ================= START GAME =================

@PY.UBOT("bola")
@PY.BOT("bola")
async def bola(_, message):
    chat_id = message.chat.id

    pemain = random.choice(PLAYERS)
    GAME[chat_id] = pemain

    await message.reply_text(
        f"""⚽ <b>TEBAK PEMAIN BOLA</b>

🧩 Clue:
<b>{pemain['clue']}</b>

✍️ Jawab dengan:
<code>.jawab nama_pemain</code>
"""
    )

# ================= JAWAB =================

@PY.UBOT("jawab")
@PY.BOT("jawab")
async def jawab(_, message):
    chat_id = message.chat.id

    if chat_id not in GAME:
        return await message.reply_text("❌ Belum ada game. Ketik <code>.bola</code>")

    jawaban = message.text.split(" ", 1)
    if len(jawaban) < 2:
        return await message.reply_text("❗ Contoh: <code>.jawab messi</code>")

    jawab = jawaban[1].lower()
    pemain = GAME[chat_id]["nama"]

    if jawab == pemain:
        user = message.from_user
        uid = user.id

        SCORE[uid] = SCORE.get(uid, 0) + 1
        del GAME[chat_id]

        await message.reply_text(
            f"""✅ <b>BENAR!</b>

👤 Pemain:
<b>{pemain.title()}</b>

🏆 Poin:
<b>{user.first_name}</b> sekarang punya <b>{SCORE[uid]}</b> poin
"""
        )
    else:
        await message.reply_text("❌ Salah! Coba lagi 😆")

# ================= SCORE =================

@PY.UBOT("bolaskor")
@PY.BOT("bolaskor")
async def skor(_, message):
    if not SCORE:
        return await message.reply_text("📭 Belum ada skor")

    text = "🏆 <b>SKOR TEBAK BOLA</b>\n\n"
    for uid, sc in SCORE.items():
        text += f"• <code>{uid}</code> : <b>{sc}</b> poin\n"

    await message.reply_text(text)