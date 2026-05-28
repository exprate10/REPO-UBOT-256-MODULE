import os
import aiohttp
from PyroUbot import *

__MODULE__ = "ᴛɪᴋᴛᴏᴋ"
__HELP__ = """
<blockquote><b>TikTok</b></b>

<b>Perintah:</b>
<code>{0}tt</code> [link tiktok] → Download video No WM.
<code>{0}ttmp3</code> [link tiktok] → Download musiknya saja.</blockquote></b>
"""

@PY.UBOT("tt|ttmp3")
@PY.TOP_CMD
async def _(client, message):
    if len(message.command) < 2:
        return await message.reply_text("<blockquote><b>📖 PANDUAN</b>\n\nKetik: <code>.tt [link]</code></blockquote>")

    link = message.text.split(None, 1)[1]
    cmd = message.command[0].lower()
    status_msg = await message.reply_text("<blockquote><b>⌛ Sedang memproses TikTok...</b></blockquote>")

    async with aiohttp.ClientSession() as session:
        try:
            # Menggunakan API yang lebih stabil untuk TikTok
            api_url = f"https://api.botcahx.eu.org/api/dowloader/tiktok?url={link}&apikey=@31Moire_mor"
            async with session.get(api_url) as resp:
                data = await resp.json()

            # Cek apakah API memberikan hasil yang valid
            if not data.get("status") or "result" not in data:
                return await status_msg.edit("<blockquote><b>⌭ API ERROR:</b> gagal mengambil data, coba lagi nanti atau ganti link.</blockquote>")

            res = data["result"]
            
            if cmd == "ttmp3":
                # Download Musik
                audio_url = res.get("audio")
                if not audio_url:
                    return await status_msg.edit("<blockquote><b>⌭ Audio ga ketemu.</b></blockquote>")
                
                await status_msg.edit("<blockquote><b>⊻ Mengirim Musik...</b></blockquote>")
                await client.send_audio(
                    chat_id=message.chat.id,
                    audio=audio_url,
                    caption=f"<blockquote><b>♧ TIKTOK MUSIC</b>\n\n<b>◉ Artis:</b> <code>{res['author'].get('nickname', 'Unknown')}</code></blockquote>"
                )
            else:
                # Download Video No WM
                video_url = res.get("video", [None])[0] # Index 0 biasanya No WM
                if not video_url:
                    return await status_msg.edit("<blockquote><b>⌭ Video ga ketemu.</b></blockquote>")
                
                await status_msg.edit("<blockquote><b>⊻ Mengirim Video...</b></blockquote>")
                await client.send_video(
                    chat_id=message.chat.id,
                    video=video_url,
                    caption=f"<blockquote><b>📹 TIKTOK NO WM</b>\n\n<b>◉ User:</b> <code>{res['author'].get('nickname', 'Unknown')}</code>\n<b>◆ Deskripsi:</b> <code>{res.get('desc', 'No Description')}</code></blockquote>"
                )

            await status_msg.delete()

        except Exception as e:
            await status_msg.edit(f"<blockquote><b>⌯ TERJADI KESALAHAN:</b>\n<code>{str(e)}</code></blockquote>")
            