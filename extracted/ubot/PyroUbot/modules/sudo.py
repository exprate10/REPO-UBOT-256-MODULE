import asyncio

from pyrogram.enums import *
from pyrogram.errors import FloodWait
from pyrogram.types import *

from PyroUbot import *

__MODULE__ = "sᴜᴅᴏ"
__HELP__ = """
<blockquote><b>👥 Sudo — RANZ PEDIA</b>

<b><b>Perintah:</b></b>
<code>{0}addsudo [@username/reply]</code>
Kasih akses user lain buat jalanin fitur userbot kamu

<code>{0}delsudo [@username/reply]</code>
Cabut akses sudo dari user

<code>{0}listsudo</code>
Lihat siapa aja yang punya akses sudo</blockquote>
"""


@PY.UBOT("addsudo")
async def addsudo_cmd(client, message):
    msg = await message.reply("<blockquote><b>◷ Lagi proses...</b></blockquote>")
    user_id = await extract_user(message)

    if not user_id:
        return await msg.edit(
            "<blockquote><b>⌭ Reply pesan user atau masukkan username/ID-nya dulu!</b></blockquote>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(f"<blockquote><b>⌭ Error:</b> {error}</blockquote>")

    sudo_users = await get_list_from_vars(client.me.id, "SUDOERS")

    if user.id in sudo_users:
        return await msg.edit(
            f"<blockquote><b>⌭ {user.first_name} udah jadi sudo user!</b></blockquote>"
        )

    try:
        await add_to_vars(client.me.id, "SUDOERS", user.id)
        return await msg.edit(
            f"<blockquote><b>⌬ {user.first_name} berhasil ditambah sebagai sudo!</b></blockquote>"
        )
    except Exception as error:
        return await msg.edit(f"<blockquote><b>⌭ Error:</b> {error}</blockquote>")


@PY.UBOT("delsudo|unsudo")
async def delsudo_cmd(client, message):
    msg = await message.reply("<blockquote><b>◷ Lagi proses...</b></blockquote>")
    user_id = await extract_user(message)

    if not user_id:
        return await msg.edit(
            "<blockquote><b>⌭ Reply pesan user atau masukkan username/ID-nya dulu!</b></blockquote>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(f"<blockquote><b>⌭ Error:</b> {error}</blockquote>")

    sudo_users = await get_list_from_vars(client.me.id, "SUDOERS")

    if user.id not in sudo_users:
        return await msg.edit(
            f"<blockquote><b>⌭ {user.first_name} bukan sudo user!</b></blockquote>"
        )

    try:
        await remove_from_vars(client.me.id, "SUDOERS", user.id)
        return await msg.edit(
            f"<blockquote><b>⌬ {user.first_name} sukses dihapus dari daftar sudo!</b></blockquote>"
        )
    except Exception as error:
        return await msg.edit(f"<blockquote><b>⌭ Error:</b> {error}</blockquote>")


@PY.UBOT("sudolist|listsudo")
async def listsudo_cmd(client, message):
    msg = await message.reply("<blockquote><b>◷ Lagi ngambil data...</b></blockquote>")
    sudo_users = await get_list_from_vars(client.me.id, "SUDOERS")

    if not sudo_users:
        return await msg.edit(
            "<blockquote><b>◆ Daftar sudo kosong!</b>\n\nBelum ada sudo user.</blockquote>"
        )

    sudo_list = []
    for uid in sudo_users:
        try:
            user = await client.get_users(int(uid))
            sudo_list.append(
                f"<b>•</b> <a href='tg://user?id={user.id}'>{user.first_name}</a> | <code>{user.id}</code>"
            )
        except Exception:
            continue

    response = (
        f"<blockquote><b>◆ Daftar Sudo User ({len(sudo_list)} orang)</b>\n\n"
        + "\n".join(sudo_list)
        + "</blockquote>"
    )
    return await msg.edit(response)
