from PyroUbot import *
import random
import requests
from pyrogram.enums import *
from pyrogram import *
from pyrogram.types import *
from io import BytesIO

__MODULE__ = "ᴄᴇᴄᴀɴ"
__HELP__ = """
<b>⦪ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴄᴇᴄᴀɴ ⦫</b>
<blockquote>
⎆ perintah :
ᚗ <code>{0}cecan</code> Query

<b>ᚗ Query:</b>
    <i>⊶ Indonesia</i>,
    <i>⊶ china</i>,
    <i>⊶ thailand</i>,
    <i>⊶ vietnam</i>,
    <i>⊶ hijaber</i>,
    <i>⊶ rose</i>,
    <i>⊶ ryujin</i>,
    <i>⊶ jiso</i>,
    <i>⊶ jeni</i>,
    <i>⊶ justinaxie</i>,
    <i>⊶ malaysia</i>,
    <i>⊶ japan</i>,
    <i>⊶ korea</i></blockquote>
"""

URLS = {
    "indonesia": "https://api.botcahx.eu.org/api/cecan/indonesia?apikey=bEcJ8rQU",
    "china": "https://api.botcahx.eu.org/api/cecan/china?apikey=bEcJ8rQU",
    "thailand": "https://api.botcahx.eu.org/api/cecan/thailand?apikey=bEcJ8rQU",
    "vietnam": "https://api.botcahx.eu.org/api/cecan/vietnam?apikey=bEcJ8rQU",
    "hijaber": "https://api.botcahx.eu.org/api/cecan/hijaber?apikey=bEcJ8rQU",
    "rose": "https://api.botcahx.eu.org/api/cecan/rose?apikey=bEcJ8rQU",
    "ryujin": "https://api.botcahx.eu.org/api/cecan/ryujin?apikey=bEcJ8rQU",
    "jiso": "https://api.botcahx.eu.org/api/cecan/jiso?apikey=bEcJ8rQU",
    "jeni": "https://api.botcahx.eu.org/api/cecan/jeni?apikey=bEcJ8rQU",
    "justinaxie": "https://api.botcahx.eu.org/api/cecan/justinaxie?apikey=bEcJ8rQU",
    "malaysia": "https://api.botcahx.eu.org/api/cecan/malaysia?apikey=bEcJ8rQU",
    "japan": "https://api.botcahx.eu.org/api/cecan/japan?apikey=bEcJ8rQU",
    "korea": "https://api.botcahx.eu.org/api/cecan/korea?apikey=bEcJ8rQU"
}

@PY.UBOT("cecan")
@PY.TOP_CMD
async def _(client, message):
    # Extract query from message
    query = message.text.split()[1] if len(message.text.split()) > 1 else None
    
    if query not in URLS:
        valid_queries = ", ".join(URLS.keys())
        await message.reply(f"Query tidak valid. Gunakan salah satu dari: {valid_queries}.")
        return

    processing_msg = await message.reply("<emoji id=5316770651720137011>🔘</emoji> Processing.....")
    
    try:
        await client.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
        response = requests.get(URLS[query])
        response.raise_for_status()
        
        photo = BytesIO(response.content)
        photo.name = 'image.jpg'
        
        await client.send_photo(message.chat.id, photo)
        await processing_msg.delete()
    except requests.exceptions.RequestException as e:
        await processing_msg.edit_text(f"Gagal mengambil gambar cecan Error: {e}")