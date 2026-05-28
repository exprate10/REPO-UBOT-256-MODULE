import asyncio
from PyroUbot import *

__MODULE__ = "ᴛʜᴀɴᴋs"
__HELP__ = """
<blockquote><b>✨ Thanks Buyer — RANZ PEDIA</b>

<b><b>Perintah:</b></b>
<code>{0}thanks</code> — Animasi terima kasih ke buyer
<code>{0}tq</code> — Versi singkat thanks
<code>{0}nx</code> — Versi santai / gaul</blockquote>
"""


async def animasi_kirim(message, frames, delay=0.4):
    msg = await message.reply(frames[0])
    last = frames[0]
    for text in frames[1:]:
        if text != last:
            try:
                await msg.edit(text)
            except Exception:
                pass
            last = text
        await asyncio.sleep(delay)


@PY.UBOT("thanks")
async def thanks_cmd(client, message):
    frames = [
        "✨",
        "✨ T",
        "✨ Te",
        "✨ Ter",
        "✨ Terim",
        "✨ Terima",
        "✨ Terima kasih",
        "✨ Terima kasih ⌗",
        "<blockquote><b>✨ Terima kasih ⌗</b>\n<b>💖 Udah beli Userbot RANZ PEDIA!</b></blockquote>",
        "<blockquote><b>✨ Terima kasih ⌗</b>\n<b>💖 Udah beli Userbot RANZ PEDIA!</b>\n<b>⟶ Semoga bermanfaat!</b></blockquote>",
    ]
    await animasi_kirim(message, frames)


@PY.UBOT("tq")
async def tq_cmd(client, message):
    frames = [
        "✨",
        "✨ T",
        "✨ TQ",
        "✨ TQ ⌗",
        "<blockquote><b>✨ TQ udah belanja di sini!</b></blockquote>",
        "<blockquote><b>✨ TQ udah belanja di sini! ⌗</b>\n<b>💖 Semoga bermanfaat ya!</b></blockquote>",
        "<blockquote><b>✨ TQ udah belanja di RANZ PEDIA! ⌗</b>\n<b>💖 Semoga bermanfaat ya!</b>\n<b>⟶ Selamat menggunakan!</b></blockquote>",
    ]
    await animasi_kirim(message, frames)


@PY.UBOT("nx")
async def nx_cmd(client, message):
    frames = [
        "✨",
        "✨ Iz",
        "✨ Izin bang",
        "✨ Izin bang 🔫",
        "<blockquote><b>✨ Izin bang 🔫</b>\n<b>RANZ PEDIA tampil bentar ya!</b></blockquote>",
        "<blockquote><b>✨ Izin bang 🔫</b>\n<b>RANZ PEDIA tampil bentar ya!</b>\n<b>⌗ Makasih udah support!</b></blockquote>",
    ]
    await animasi_kirim(message, frames)
