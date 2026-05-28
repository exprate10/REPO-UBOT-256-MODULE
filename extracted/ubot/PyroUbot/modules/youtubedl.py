import aiohttp
from PyroUbot import *

__MODULE__ = "ʏᴏᴜᴛᴜʙᴇ"
__HELP__ = """
<blockquote><b><b>Youtube</b></b>

<b>Perintah:</b>
<code>{0}ytv</code> [link] → Download Video YouTube.
<code>{0}yta</code> [link] → Download Audio YouTube.</blockquote></b>
"""

@PY.UBOT("ytv|yta")
@PY.TOP_CMD
async def _(client, message):
    if len(message.command) < 2:
        return await message.reply_text("<blockquote><b>📖 PANDUAN</b>\n\nKetik: <code>.ytv [link]</code> atau <code>.yta [link]</code></blockquote>")

    link = message.text.split(None, 1)[1]
    cmd = message.command[0].lower()
    status_msg = await message.reply_text("<blockquote><b>⌛ Sedang memproses YouTube...</b></blockquote>")

    async with aiohttp.ClientSession() as session:
        try:
            # Menggunakan API yang stabil khusus untuk downloader
            api_url = f"https://api.botcahx.eu.org/api/dowloader/yt?url={link}&apikey=@31Moire_mor"
            async with session.get(api_url) as resp:
                data = await resp.json()

            # Pengecekan agar tidak error 'result'
            if not data.get("status") or "result" not in data:
                return await status_msg.edit("<blockquote><b>⌭ API ERROR:</b> gagal mengambil data, pastikan link benar atau API tidak limit.</blockquote>")

            res = data["result"]
            
            if cmd == "yta":
                # Kirim Audio (MP3)
                if not res.get("mp3"):
                    return await status_msg.edit("<blockquote><b>⌭ gagal:</b> File MP3 tidak tersedia untuk video ini.</blockquote>")
                
                await status_msg.edit("<blockquote><b>⊻ Mengirim Audio YouTube...</b></blockquote>")
                await client.send_audio(
                    chat_id=message.chat.id,
                    audio=res["mp3"],
                    caption=f"<blockquote><b>♧ YOUTUBE MP3</b>\n\n<b>⌖ Judul:</b> <code>{res.get('title', 'Unknown')}</code></blockquote>"
                )
            else:
                # Kirim Video (MP4)
                if not res.get("mp4"):
                    return await status_msg.edit("<blockquote><b>⌭ gagal:</b> File MP4 tidak tersedia.</blockquote>")
                
                await status_msg.edit("<blockquote><b>⊻ Mengirim Video YouTube...</b></blockquote>")
                await client.send_video(
                    chat_id=message.chat.id,
                    video=res["mp4"],
                    caption=f"<blockquote><b>📹 YOUTUBE VIDEO</b>\n\n<b>⌖ Judul:</b> <code>{res.get('title', 'Unknown')}</code></blockquote>"
                )

            await status_msg.delete()

        except Exception as e:
            await status_msg.edit(f"<blockquote><b>⌯ TERJADI KESALAHAN:</b>\n<code>{str(e)}</code></blockquote>")
            