import socket
from pyrogram import *
from pyrogram import Client, filters
from PyroUbot import PY

__MODULE__ = "ᴄᴇᴋ ɪᴘ"
__HELP__ = """
<blockquote><b><b>Cek IP Website</b></b>

<b>Perintah:</b> <code>{0}cekip</code> [domain]
Penjelasan: untuk mendapatkan alamat IP dari domain yang diberikan</blockquote></b>
"""

@PY.UBOT("cekip")
@PY.TOP_CMD
async def cek_ip_command(client, message):
    # Ambil argumen dari pesan
    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        await message.reply_text(
            "<blockquote><b>⌯ Gunakan format: cekip [domain]</b></blockquote>"
        )
        return

    domain = args[1]

    try:
        ip_address = socket.gethostbyname(domain)
        result_text = f"<blockquote><b>⌖ **Hasil Pengecekan IP untuk:** `{domain}`\n\n◎ IP Address: `{ip_address}`</b></blockquote>"
    except Exception as e:
        result_text = f"⌭ Terjadi kesalahan: {str(e)}"

    await message.reply_text(result_text)