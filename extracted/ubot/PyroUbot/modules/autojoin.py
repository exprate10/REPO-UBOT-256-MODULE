import asyncio
from PyroUbot import *

__MODULE__ = "ᴊᴏɪɴᴇʀ"
__HELP__ = """
<blockquote><b>Bantuan Untuk Joiner</b>

Perintah:
<code>{0}join</code> [reply link grup] → Join ke grup yang ada di pesan tersebut.
Catatan: Bisa deteksi banyak link sekaligus dalam satu pesan.</blockquote></b>
"""

@PY.UBOT("join")
@PY.TOP_CMD
async def _(client, message):
    # Validasi reply
    if not message.reply_to_message or not message.reply_to_message.text:
        return await message.reply_text("<blockquote><b>❌ GAGAL</b>\nBalas ke pesan yang berisi link grup atau username (misal: @roomiqbal).</blockquote>")

    status_msg = await message.reply_text("<blockquote><b>⏳ Sedang memproses permintaan join...</b></blockquote>")
    
    # Ambil semua kata dalam pesan yang di-reply
    text = message.reply_to_message.text
    links = []
    for word in text.split():
        if word.startswith("@"):
            links.append(word.replace("@", ""))
        elif "t.me/" in word:
            links.append(word.split("/")[-1])

    if not links:
        return await status_msg.edit("<blockquote><b>❌ TIDAK ADA LINK</b>\nTidak ditemukan username atau link grup yang valid.</blockquote>")

    success = 0
    failed = 0
    
    for chat in links:
        try:
            await client.join_chat(chat)
            success += 1
            await asyncio.sleep(2) # Jeda 2 detik agar tidak kena limit/spam
        except Exception:
            failed += 1
            continue

    hasil = (
        f"<blockquote><b>✅ PROSES JOIN SELESAI</b>\n\n"
        f"<b>• Berhasil:</b> <code>{success} Grup</code>\n"
        f"<b>• Gagal:</b> <code>{failed} Grup</code>\n\n"
        f"<i>Info: Gagal biasanya karena grup privat atau akun sudah kena limit.</i></blockquote>"
    )
    await status_msg.edit(hasil)
    