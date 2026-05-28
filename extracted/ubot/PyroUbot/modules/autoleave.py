import asyncio
from PyroUbot import *

__MODULE__ = "ʟᴇᴀᴠᴇʀ"
__HELP__ = """
<blockquote><b>Bantuan Untuk Leaver</b>

Perintah:
<code>{0}leave</code> → Keluar dari grup ini.
<code>{0}kickme</code> → Keluar dari grup ini (Sama saja).
<code>{0}leaveall</code> → Keluar dari semua grup yang ubot kamu masuki.</blockquote></b>
"""

@PY.UBOT("leave|kickme")
@PY.TOP_CMD
async def _(client, message):
    await message.reply_text("<blockquote><b>👋 Selamat tinggal!</b>\nUbot akan keluar dari grup ini.</blockquote>")
    await client.leave_chat(message.chat.id)

@PY.UBOT("leaveall")
@PY.TOP_CMD
async def _(client, message):
    status = await message.reply_text("<blockquote><b>⏳ Memulai proses keluar dari semua grup...</b></blockquote>")
    count = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            chat_id = dialog.chat.id
            if chat_id == message.chat.id: # Jangan keluar dulu dari grup tempat perintah dijalankan
                continue
            try:
                await client.leave_chat(chat_id)
                count += 1
                await asyncio.sleep(1) # Delay biar gak limit
            except:
                continue
    
    await status.edit(f"<blockquote><b>✅ BERHASIL KELUAR</b>\nKeluar dari <code>{count}</code> grup.</blockquote>")
    