import os
import aiohttp
from PyroUbot import *

__MODULE__ = "ғᴀᴄᴇ ᴅᴇᴛᴇᴄᴛ"
__HELP__ = """
<blockquote><b>Bantuan Untuk Face Detect</b>

Perintah:
<code>{0}face</code> [reply foto] → Deteksi wajah dan info lainnya.</blockquote></b>
"""

@PY.UBOT("face")
@PY.TOP_CMD
async def _(client, message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        return await message.reply_text("<blockquote>Balas ke foto wajah seseorang!</blockquote>")

    status = await message.reply_text("<blockquote><b>🔍 Menganalisis wajah...</b></blockquote>")
    path = await message.reply_to_message.download()

    async with aiohttp.ClientSession() as session:
        try:
            with open(path, 'rb') as f:
                form = aiohttp.FormData()
                form.add_field('file', f)
                api_url = f"https://api.botcahx.eu.org/api/tools/facedetect?apikey=@31Moire_mor"
                async with session.post(api_url, data=form) as resp:
                    data = await resp.json()

            if not data.get("status") or "result" not in data:
                return await status.edit("<blockquote><b>❌ Gagal!</b> Wajah tidak terdeteksi atau API limit.</blockquote>")

            res = data["result"]
            hasil = (
                f"<blockquote><b>👤 HASIL DETEKSI WAJAH</b>\n\n"
                f"<b>👨‍👩‍👦 Jumlah Wajah:</b> <code>{res.get('face_count', 0)}</code>\n"
                f"<b>🎂 Perkiraan Umur:</b> <code>{res.get('age', 'Tidak diketahui')}</code>\n"
                f"<b>🎭 Gender:</b> <code>{res.get('gender', 'Tidak diketahui')}</code></blockquote>"
            )
            await status.edit(hasil)
        except Exception as e:
            await status.edit(f"<blockquote><b>⚠️ Error:</b> <code>{str(e)}</code></blockquote>")
        finally:
            if os.path.exists(path):
                os.remove(path)
                