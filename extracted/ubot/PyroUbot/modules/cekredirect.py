import requests
from PyroUbot import *

__MODULE__ = "ᴄᴇᴋ ʀᴇᴅɪʀᴇᴄᴛ"
__HELP__ = """
<b>⦪ <blockquote>⎆ <b>Perintah:</b>
ᚗ <code>{0}redirect</code> url
⊶ Untuk mengecek link asli shorturl.</blockquote>
"""

@PY.UBOT("redirect")
async def cek_redirect(client, message):
    if len(message.command) < 2:
        return await message.reply("**Usage:** `.cekredirect <url>`\nContoh: `.cekredirect https://tinyurl.com/bdtf7se9`")

    url = message.command[1]
    api_url = f"https://api.botcahx.eu.org/api/tools/cekredirect?url={url}&apikey=moire"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            if data.get("status"):
                hasil = data.get("result", [])
                teks = f"⌖ **Hasil Redirect:**\n\n"
                for idx, item in enumerate(hasil, 1):
                    teks += f"**{idx}.** `{item['url']}`"
                    if "status" in item:
                        teks += f"-> `{item['status']}`"
                    teks += "\n"
                await message.reply(f"<blockquote>{teks}</blockquote>")
            else:
                await message.reply("⌯ gagal mengambil data redirect.")
        else:
            await message.reply("⌭ API tidak dapat diakses, coba lagi nanti.")
    except Exception as e:
        await message.reply(f"🚨 Terjadi kesalahan:\n`{str(e)}`")
