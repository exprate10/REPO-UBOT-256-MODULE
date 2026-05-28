import os
from PyroUbot import *

__MODULE__ = "sᴛɪᴄᴋᴇʀ ᴛᴏ ɪᴍɢ"
__HELP__ = """
<blockquote><b>Bantuan Untuk Converter</b>

Perintah:
<code>{0}toimg</code> [reply stiker] → Ubah stiker menjadi foto JPG.</blockquote></b>
"""

@PY.UBOT("toimg")
@PY.TOP_CMD
async def _(client, message):
    if not message.reply_to_message or not message.reply_to_message.sticker:
        return await message.reply_text("<blockquote>Balas ke stiker yang mau dijadikan foto.</blockquote>")
    
    status = await message.reply_text("<blockquote>⏳ Sedang mengonversi...</blockquote>")
    path = await message.reply_to_message.download()
    output = "converted_photo.jpg"
    
    # Menggunakan perintah sistem untuk convert cepat
    os.system(f"ffmpeg -i {path} {output} -y")
    
    await client.send_photo(message.chat.id, output, caption="<blockquote>✅ Berhasil diubah ke foto!</blockquote>")
    await status.delete()
    os.remove(path)
    os.remove(output)
    