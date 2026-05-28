import random
from pyrogram import *
from pyrogram import Client, filters
from PyroUbot import PY

__MODULE__ = "ᴄᴇᴋ ᴀɢᴀᴍᴀ"
__HELP__ = """
<blockquote><b>Cek Agama</b></b>

<b>Perintah:</b>
<code>{0}cekagama [nama]</code> → DETEKSI AGAMA DARI NAMA  

Sumber: Random generator berdasarkan nama.</blockquote></b>
"""

AGAMA_LIST = [
    "HINDU","ATEIS (GAK PUNYA AGAMA","ISLAM","KRISTEN","BUDHA","KATOLIK","KRISTEN PROTESTAN","ISLAM KTP","KONGHUCU",
]

@PY.UBOT("cekagama")
@PY.TOP_CMD
async def cek_agama(client, message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply_text("<blockquote><b>⌯ Gunakan format: .cekagama [nama]</blockquote></b>")

    nama = args[1]
    agama = random.choice(AGAMA_LIST)
    hasil = f'''<blockquote><b>
    HASIL DETEKSI AGAMA DARI {nama}
    ╭───────────────────────
    ├ ɴᴀᴍᴀ : `{nama}`
    ├ ᴀɢᴀᴍᴀ: `{agama}`
    ├ sᴇʟᴀᴍᴀᴛ ʏᴀ ᴀɢᴀᴍᴀ ɴʏᴀ ᴄᴏᴄᴏᴋ ᴋᴏᴋ
    ╰────────────────────────
    ɴᴏᴛᴇ ᴍᴀᴀғ ʏᴀ {nama} ᴄᴜᴍᴀ ʙᴇᴄᴀɴᴅᴀ ᴋᴏᴋ 
    
    </blockquote></b>'''
    await message.reply_text(hasil)
