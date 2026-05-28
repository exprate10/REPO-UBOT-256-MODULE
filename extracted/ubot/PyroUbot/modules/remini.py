import requests
import os
from PyroUbot import *
from pyrogram.types import Message

__MODULE__ = "ʀᴇᴍɪɴɪ"
__HELP__ = """
<blockquote><b>
<blockquote><b><b>Perintah:</b> <code>{0}ʀᴇᴍɪɴɪ</code> ᴀᴛᴀᴜ <code>{0}ʜᴅ</code>
    ᴜɴᴛᴜᴋ ᴍᴇɴᴊᴇʀɴɪʜᴋᴀɴ ɢᴀᴍʙᴀʀ (ғᴜʟʟ ᴘʀᴇᴍɪᴜᴍ)</b></blockquote>
"""

@PY.UBOT("remini|hd")
@PY.TOP_CMD
async def process_image(client, message):
    # 1. Validasi: Harus reply ke foto
    if not message.reply_to_message or not message.reply_to_message.photo:
        return await message.reply("<blockquote><b>ʀᴇᴘʟʏ ɢᴀᴍʙᴀʀ ʏᴀɴɢ ᴍᴀᴜ ᴅɪ ʜᴅ ɪɴ ᴋɪɴɢ</b></blockquote>")

    msg = await message.reply("<blockquote><b>sᴇᴅᴀɴɢ ᴅɪᴘʀᴏsᴇs ᴍᴇɴᴊᴀᴅɪ ʜᴅ, ᴍᴏʜᴏɴ ᴛᴜɴɢɢᴜ...</b></blockquote>")

    file_path = None
    try:
        # 2. Download foto dari Telegram ke VPS
        file_path = await message.reply_to_message.download()
        
        # 3. Konfigurasi API
        api_key = "@31Moire_mor"
        # Gunakan endpoint maker/remini untuk hasil HD maksimal
        api_url = f"https://api.botcahx.eu.org/api/maker/remini?apikey={api_key}"
        
        # 4. Upload file ke API menggunakan Multipart Form Data
        with open(file_path, "rb") as img_file:
            files = {"file": img_file}
            response = requests.post(api_url, files=files)

        # 5. Cek respon dari server
        if response.status_code == 200:
            res_data = response.json()
            
            if res_data.get("status") is True:
                # Ambil URL hasil HD
                image_hd_url = res_data.get("result")
                
                # Kirim balik ke user
                await client.send_photo(
                    chat_id=message.chat.id,
                    photo=image_hd_url,
                    caption="<blockquote><b>sᴜᴅᴀʜ ᴊᴀᴅɪ ʜᴅ ᴋɪɴɢ, sɪʟᴀʜᴋᴀɴ ᴅɪ ᴄᴇᴋ</b></blockquote>",
                    reply_to_message_id=message.id
                )
                await msg.delete()
            else:
                await msg.edit("<blockquote><b>ɢᴀɢᴀʟ ᴍᴇᴍᴘʀᴏsᴇs ɢᴀᴍʙᴀʀ, ᴍᴜɴɢᴋɪɴ ʟɪᴍɪᴛ ᴀᴘɪ ʜᴀʙɪs</b></blockquote>")
        else:
            await msg.edit(f"<blockquote><b>sᴇʀᴠᴇʀ ᴀᴘɪ ᴇʀᴏʀ: {response.status_code}</b></blockquote>")

    except Exception as e:
        await msg.edit(f"<blockquote><b>ᴛᴇʀᴊᴀᴅɪ ᴋᴇsᴀʟᴀʜᴀɴ ᴋɪɴɢ:</b></blockquote>\n<code>{str(e)}</code>")
    
    finally:
        # 6. Bersihkan file sampah di VPS biar gak penuh
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

