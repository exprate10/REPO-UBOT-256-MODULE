import requests
from pyrogram import Client, filters
from PyroUbot import *

__MODULE__ = "ғᴀᴋᴇ ᴅᴀᴛᴀ"
__HELP__ = """
<b>⦪ <blockquote>⎆ <b>Perintah:</b>
ᚗ <code>{0}fakedata</code>
⊶ untuk membuat fake data pribadi</blockquote>
"""
@PY.UBOT("fakedata")
async def generate_fake_data(client, message):
    API_URL = "https://api.siputzx.my.id/api/tools/fake-data"
    params = {
        "type": "person",
        "count": 5
    }
    
    try:
        response = requests.get(API_URL, params=params)
        data = response.json()
        
        if data.get("status"):
            fake_list = data.get("data", [])
            result = "<blockquote>**Fake Profiles:**\n"
            
            for i, fake in enumerate(fake_list, start=1):
                result += f"\n**{i}.**\n"
                result += f"◉ **Name:** `{fake['name']}`\n"
                result += f"📧 **Email:** `{fake['email']}`\n"
                result += f"📞 **Phone:** `{fake['phone']}`\n"
                result += f"🎂 **Birth Date:** `{fake['birthDate']}`\n"
                result += f"⚧ **Gender:** `{fake['gender']}`</blockquote>\n"
            
            await message.reply_text(result)
        else:
            await message.reply_text("gagal mengambil data Fake Data.")
    
    except Exception as e:
        await message.reply_text(f"Terjadi kesalahan: {e}")
                
