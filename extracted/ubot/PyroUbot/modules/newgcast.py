import asyncio
from PyroUbot import *
from pyrogram.enums import ChatType, ChatMemberStatus

__MODULE__ = "𝙶𝙲𝙰𝚂𝚃 𝙽𝙴𝚆"
__HELP__ = """
<blockquote><b>Gcast New</b>

<b>Perintah:</b> <code>{0}bc gc</code> [reply pesan]
Kirim ke semua grup.

<b>Perintah:</b> <code>{0}bc pv</code> [reply pesan]
Kirim ke semua chat pribadi.

<b>Perintah:</b> <code>{0}bc adm</code> [reply pesan]
Kirim ke grup yang kamu jadi admin.</blockquote>
"""

def get_message(message):
    return (
        message.reply_to_message
        if message.reply_to_message
        else "" if len(message.command) < 2
        else " ".join(message.command[1:])
    )

@PY.UBOT("bc")
async def _(c, m):
    done = 0

    if len(m.command) != 2:
        return await m.reply(
            "<blockquote><b>⌭ Format salah.</b>\n"
            "Pakai: <code>.bc [gc/adm/pv]</code> balas ke pesan.</blockquote>"
        )

    send = get_message(m)
    if not send or not m.reply_to_message:
        return await m.reply(
            "<blockquote><b>⌭ Balas ke pesan dulu ya!</b></blockquote>",
            quote=True,
        )

    blacklist = await get_chat(c.me.id)
    mode      = m.command[1].lower()

    if mode not in ("gc", "pv", "adm"):
        return await m.reply(
            "<blockquote><b>⌭ Mode salah.</b>\n"
            "Pilihan: <code>gc</code> | <code>pv</code> | <code>adm</code></blockquote>"
        )

    Haku = await m.reply("<blockquote><b>◷ Lagi proses...</b></blockquote>")

    try:
        if mode == "gc":
            async for dialog in c.get_dialogs():
                if dialog.chat.type in (ChatType.SUPERGROUP, ChatType.GROUP):
                    chat_id = dialog.chat.id
                    await asyncio.sleep(0.1)
                    if chat_id not in blacklist:
                        try:
                            await send.copy(chat_id)
                            done += 1
                        except Exception:
                            pass
            await Haku.edit(
                f"<blockquote><b>⌬ Selesai kirim ke {done} grup.</b>\n\n"
                f"<b>By: RANZ PEDIA</b></blockquote>"
            )

        elif mode == "pv":
            async for dialog in c.get_dialogs():
                if dialog.chat.type == ChatType.PRIVATE:
                    chat_id = dialog.chat.id
                    await asyncio.sleep(0.1)
                    if chat_id not in blacklist:
                        try:
                            await send.copy(chat_id)
                            done += 1
                        except Exception:
                            pass
            await Haku.edit(
                f"<blockquote><b>⌬ Selesai kirim ke {done} chat pribadi.</b>\n\n"
                f"<b>By: RANZ PEDIA</b></blockquote>"
            )

        elif mode == "adm":
            async for dialog in c.get_dialogs():
                if dialog.chat.type in (ChatType.SUPERGROUP, ChatType.GROUP):
                    chat_id = dialog.chat.id
                    await asyncio.sleep(0.1)
                    try:
                        member = await c.get_chat_member(chat_id, "me")
                        if member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
                            await send.copy(chat_id)
                            done += 1
                    except Exception:
                        pass
            await Haku.edit(
                f"<blockquote><b>⌬ Selesai kirim ke {done} grup (sebagai admin).</b>\n\n"
                f"<b>By: RANZ PEDIA</b></blockquote>"
            )

    except IndexError:
        await Haku.edit(
            "<blockquote><b>⌭ Format salah.</b>\n"
            "Pakai: <code>.bc gc/adm/pv</code> balas ke pesan.</blockquote>"
        )
