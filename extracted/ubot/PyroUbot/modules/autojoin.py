import asyncio
from PyroUbot import *

__MODULE__ = "ᴊᴏɪɴᴇʀ"
__HELP__ = """
<blockquote><b>Joiner</b>

<b>Perintah:</b>
<code>{0}join</code> [reply link grup] — Join ke grup yang ada di pesan yang di-reply.
Bisa deteksi banyak link sekaligus dalam satu pesan.</blockquote>
"""

@PY.UBOT("join")
@PY.TOP_CMD
async def _(client, message):
    if not message.reply_to_message or not message.reply_to_message.text:
        return await message.reply(
            "<blockquote><b>⌭ Gagal</b>\n"
            "Balas ke pesan yang berisi link grup atau username dulu.</blockquote>"
        )

    status_msg = await message.reply("<blockquote><b>◷ Lagi proses permintaan join...</b></blockquote>")

    text  = message.reply_to_message.text
    links = []
    for word in text.split():
        if word.startswith("@"):
            links.append(word.replace("@", ""))
        elif "t.me/" in word:
            links.append(word.split("/")[-1])

    if not links:
        await status_msg.edit(
            "<blockquote><b>⌭ Ga Ada Link</b>\n"
            "Ga ketemu username atau link grup yang valid.</blockquote>"
        )
        return

    success = 0
    failed  = 0

    for chat in links:
        try:
            await client.join_chat(chat)
            success += 1
            await asyncio.sleep(2)
        except Exception:
            failed += 1
            continue

    await status_msg.edit(
        f"<blockquote><b>⌬ Proses Join Selesai</b>\n\n"
        f"<b>Berhasil :</b> <code>{success} Grup</code>\n"
        f"<b>Gagal    :</b> <code>{failed} Grup</code>\n\n"
        f"<i>Gagal biasanya karena grup privat atau akun kena limit.</i></blockquote>"
    )
