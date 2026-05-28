from PyroUbot import *

__MODULE__ = "ʙɪɴᴇʀ"
__HELP__ = """
<blockquote><b>Bantuan Untuk Biner</b>

Perintah:
<code>{0}tobin</code> [teks] → Ubah teks jadi kode biner.
<code>{0}frombin</code> [biner] → Ubah biner kembali jadi teks.</blockquote></b>
"""

@PY.UBOT("tobin")
@PY.TOP_CMD
async def _(client, message):
    if len(message.command) < 2:
        return await message.reply_text("<blockquote>Masukkan teksnya!</blockquote>")
    text = message.text.split(None, 1)[1]
    res = ' '.join(format(ord(i), '08b') for i in text)
    await message.reply_text(f"<blockquote><b>📟 TEXT TO BINARY</b>\n\n<code>{res}</code></blockquote>")

@PY.UBOT("frombin")
@PY.TOP_CMD
async def _(client, message):
    if len(message.command) < 2:
        return await message.reply_text("<blockquote>Masukkan kode binernya!</blockquote>")
    text = message.text.split(None, 1)[1].replace(" ", "")
    try:
        res = ''.join(chr(int(text[i:i+8], 2)) for i in range(0, len(text), 8))
        await message.reply_text(f"<blockquote><b>📖 BINARY TO TEXT</b>\n\n<code>{res}</code></blockquote>")
    except:
        await message.reply_text("<blockquote>❌ Kode biner tidak valid!</blockquote>")
        