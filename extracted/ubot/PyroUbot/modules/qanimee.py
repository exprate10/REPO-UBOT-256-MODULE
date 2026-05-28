import requests
from pyrogram import Client, filters
from PyroUbot import *

__MODULE__ = "ϙᴜᴏᴛᴇs ᴀɴɪᴍᴇ"
__HELP__ = """
<b>⦪ <blockquote>⎆ <b>Perintah:</b>
ᚗ <code>{0}qanime</code></blockquote>
"""

@PY.UBOT("qanime")
async def quotes_anime(client, message):
    API_URL = "https://api.siputzx.my.id/api/r/quotesanime"
    params = {
        "type": "quotesanime",
        "count": 0
    }
    
    try:
        response = requests.get(API_URL, params=params)
        data = response.json()
        if data.get("status"):
            quotes_list = data.get("data", [0])
            quotes = random.choice(quotes_list)
            result = "**Quotes Anime**\n"
            
            for quotes in quotes_list:
                result += f"<blockquote>\n<emoji id=6206162931663508973>💜</emoji><emoji id=6204012166660494973>💜</emoji> **Karakter :** `{quotes['karakter']}`\n"
                result += f"<emoji id=6203909748870354847>💜</emoji><emoji id=6203792139780887891>💜</emoji> **Anime :** `{quotes['anime']}`\n"
                result += f"<emoji id=6203959201123800232>💜</emoji><emoji id=6204000918141146257>💜</emoji> **Episode :** `{quotes['episode']}`\n"
                result += f"<emoji id=6203978081800033988>💜</emoji><emoji id=6206004318521267252>💜</emoji> **Quotes :** `{quotes['quotes']}`\n"
                result += f"<emoji id=6206193146758435609>💜</emoji><emoji id=6203731219964761845>💜</emoji> [**Link :**]({quotes['link']})\n</blockquote>"
            
            await message.reply_text(result)
        else:
            await message.reply_text("gagal mengambil data Quotes.")
    
    except Exception as e:
        await message.reply_text(f"Terjadi kesalahan: {e}")
