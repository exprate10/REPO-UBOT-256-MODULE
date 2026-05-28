import asyncio
from PyroUbot import *

__MODULE__ = "ʙʀᴏᴀᴅᴄᴀsᴛ"
__HELP__ = """
<blockquote><b>◉ Broadcast Member — RANZ PEDIA</b>

<b>Perintah:</b></b>
<code>{0}bcmem</code> <i>(reply pesan/media)</i>
Sebar pesan ke semua member via PM

<code>{0}stopbc</code>
Stop proses broadcast yang lagi jalan</blockquote>
"""

bc_status = []


@PY.UBOT("bcmem")
@PY.TOP_CMD
async def bcmem_cmd(client, message):
    global bc_status

    if not message.reply_to_message:
        return await message.reply(
            "<blockquote><b>⌭ gagal!</b>\n\nReply dulu ke pesan atau media yang mau disebar!</blockquote>"
        )

    chat_id = message.chat.id
    status_msg = await message.reply(
        "<blockquote><b>◉ Mulai broadcast ke semua member via PM...</b></blockquote>"
    )

    if client.me.id in bc_status:
        bc_status.remove(client.me.id)

    success = 0
    failed = 0

    async for member in client.get_chat_members(chat_id):
        if client.me.id in bc_status:
            break
        if member.user.is_bot or member.user.is_self:
            continue
        try:
            await message.reply_to_message.copy(member.user.id)
            success += 1
            await asyncio.sleep(3)
        except Exception:
            failed += 1
            continue

    await status_msg.edit(
        f"<blockquote><b>⌬ Broadcast Selesai!</b>\n\n"
        f"<b>Berhasil:</b> {success} member\n"
        f"<b>gagal:</b> {failed} member\n\n"
        f"<b>Pesan udah dikirim satu per satu ke PM.</b></blockquote>"
    )


@PY.UBOT("stopbc")
@PY.TOP_CMD
async def stopbc_cmd(client, message):
    bc_status.append(client.me.id)
    await message.reply(
        "<blockquote><b>⊠ Broadcast dihentikan!</b></blockquote>"
    )
