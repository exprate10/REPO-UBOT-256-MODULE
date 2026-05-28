import os
import aiohttp
import asyncio
from PyroUbot import *

__MODULE__ = "sᴘᴏᴛɪғʏ ᴘʀᴏ"
__HELP__ = """
<blockquote><b>Spotify Pro</b></b>

<b>Perintah:</b>
<code>{0}spotify</code> [judul lagu] → Cari dan download lagu Spotify menjadi MP3.</blockquote></b>
"""

@PY.UBOT("spotify")
@PY.TOP_CMD
async def _(client, message):
    if len(message.command) < 2:
        return await message.reply_text("<blockquote><b>📖 PANDUAN</b>\n\nKetik: <code>.spotify judul lagu</code></blockquote>")

    query = message.text.split(None, 1)[1]
    status_msg = await message.reply_text("<blockquote><b>⌖ Sedang mencari lagu...</b></blockquote>")

    async with aiohttp.ClientSession() as session:
        try:
            # Step 1: Cari Lagu
            search_api = f"https://api.botcahx.eu.org/api/search/spotify?query={query}&apikey=@31Moire_mor"
            async with session.get(search_api) as resp:
                search_data = await resp.json()

            # Validasi hasil pencarian
            if not search_data.get("status") or not search_data["result"]["status"] or not search_data["result"]["data"]:
                return await status_msg.edit("<blockquote><b>⌭ Lagu ga ketemu.</b></blockquote>")

            track = search_data["result"]["data"][0]
            track_url = track["url"]

            # Step 2: Download Audio
            await status_msg.edit("<blockquote><b>⊻ Sedang mengunduh file audio...</b></blockquote>")
            download_api = f"https://api.botcahx.eu.org/api/download/spotify?url={track_url}&apikey=@31Moire_mor"
            async with session.get(download_api) as resp:
                dl_data = await resp.json()

            # Validasi hasil download
            if not dl_data.get("status") or not dl_data["result"]["status"]:
                return await status_msg.edit("<blockquote><b>⌭ gagal mengonversi lagu.</b></blockquote>")

            res = dl_data["result"]["data"]
            file_url = res["url"]
            file_name = f"{res['title']} - {res['artist']['name']}.mp3".replace("/", "-")

            # Step 3: Proses Download ke VPS
            async with session.get(file_url) as audio_resp:
                if audio_resp.status != 200:
                    return await status_msg.edit("<blockquote><b>⌭ Server menolak akses download (403).</b></blockquote>")
                with open(file_name, "wb") as f:
                    f.write(await audio_resp.read())

            # Step 4: Kirim Audio ke Chat
            await client.send_audio(
                chat_id=message.chat.id,
                audio=file_name,
                caption=(
                    f"<blockquote><b>♧ SPOTIFY DOWNLOADER</b>\n\n"
                    f"<b>♧ Judul:</b> <code>{res['title']}</code>\n"
                    f"<b>◉ Artis:</b> <code>{res['artist']['name']}</code>\n"
                    f"<b>◷ Durasi:</b> <code>{res['duration']}</code>\n\n"
                    f"<b>🎧 <a href='{track_url}'>Buka di Spotify</a></b></blockquote>"
                )
            )

            await status_msg.delete()
            if os.path.exists(file_name):
                os.remove(file_name)

        except Exception as e:
            await status_msg.edit(f"<blockquote><b>⌯ Terjadi Kesalahan:</b>\n<code>{str(e)}</code></blockquote>")
            