from PyroUbot import *

__MODULE__ = "cᴇᴋ sᴛɪᴄᴋᴇʀ"
__HELP__ = f"""
<blockquote><b>Sticker Inspector</b>

Perintah:
  • {0}sticker
    └ Reply ke sticker untuk melihat informasinya

Info yang ditampilkan:
  • Sticker ID
  • Emoji
  • Nama Pack
  • Animated / Video</blockquote>
"""

@PY.UBOT("sticker")
async def sticker_inspector(client, message):
    if not message.reply_to_message:
        return await message.reply(
            "<b>Reply ke sticker nya bang, hdh</b>"
        )

    sticker = message.reply_to_message.sticker
    if not sticker:
        return await message.reply(
            "<b>Pesan tersebut bukan sticker</b>"
        )

    text = f"""
<blockquote><b>🎨 STICKER INSPECTOR</b>

• Sticker ID :
<code>{sticker.file_id}</code>

• Emoji      : {sticker.emoji or 'ga ada'}
• Pack Name  : {sticker.set_name or 'ga ada'}

• Animated   : {"⌬ Ya" if sticker.is_animated else "⌭ Tidak"}
• Video      : {"⌬ Ya" if sticker.is_video else "⌭ Tidak"}</blockquote>
"""

    await message.reply(text)