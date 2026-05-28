import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from PyroUbot import *

__MODULE__ = "𝙲𝙻𝙾𝙽𝙴"
__HELP__ = """
<blockquote><b>Clone</b>

<b>Perintah:</b> <code>{0}clone</code> @username
Nyamar jadi orang lain.

<b>Perintah:</b> <code>{0}clone kembali</code>
Balik ke identitas asli.</blockquote>
"""

STORAGE = {}

DEV_LIST = ["Rilesya", "ranzpedia_bot"]

@PY.UBOT("clone")
async def impostor(client: Client, message: Message):
    user_id = message.from_user.id
    inputArgs = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""

    for dev in DEV_LIST:
        if f"@{dev}" in inputArgs or dev in inputArgs:
            xx = await message.reply("<blockquote><b>⌭ Ga bisa nyamar jadi developer!</b></blockquote>")
            return

    xx = await message.reply("<blockquote><b>◷ Lagi proses...</b></blockquote>")

    if "kembali" in inputArgs:
        if user_id not in STORAGE:
            await asyncio.sleep(0.8)
            await xx.delete()
            await client.send_message(
                message.chat.id,
                "<blockquote><b>⌭ Kamu harus clone dulu sebelum balik!</b></blockquote>",
                reply_to_message_id=message.id,
            )
            return
        await xx.edit("<blockquote><b>◷ Lagi balikkin identitas asli...</b></blockquote>")
        await update_profile(client, STORAGE[user_id], restore=True)
        del STORAGE[user_id]
        await xx.edit("<blockquote><b>⌬ Identitas asli udah balik!</b></blockquote>")
        return

    if inputArgs:
        try:
            user = await client.get_users(inputArgs)
        except Exception:
            await xx.edit("<blockquote><b>⌭ Username atau ID ga valid.</b></blockquote>")
            return
        userObj = await client.get_chat(user.id)
    elif message.reply_to_message:
        reply_user = message.reply_to_message.from_user
        if not reply_user:
            await xx.edit("<blockquote><b>⌭ Ga bisa nyamar jadi admin anonim.</b></blockquote>")
            return
        userObj = await client.get_chat(reply_user.id)
    else:
        await xx.edit("<blockquote><b>⌭ Pakai <code>.clone @username</code> atau reply pesan seseorang.</b></blockquote>")
        return

    if user_id not in STORAGE:
        my_profile = await client.get_chat("me")
        my_photos  = [p async for p in client.get_chat_photos("me")]
        STORAGE[user_id] = {"profile": my_profile, "photos": my_photos}

    await xx.edit("<blockquote><b>◷ Lagi nyuri identitas...</b></blockquote>")
    await update_profile(client, userObj)
    await xx.edit("<blockquote><b>⌬ Berhasil! Sekarang gw jadi kamu.</b></blockquote>")


async def update_profile(client: Client, userObj, restore=False):
    if restore:
        profile_data = userObj["profile"]
        photos       = userObj["photos"]
        await client.update_profile(
            first_name=profile_data.first_name or "Deleted Account",
            last_name=profile_data.last_name   or "",
            bio=profile_data.bio               or "",
        )
        if photos:
            try:
                pfp = await client.download_media(photos[0].file_id)
                await client.set_profile_photo(photo=pfp)
            except Exception:
                pass
        return

    first_name = userObj.first_name or "Deleted Account"
    last_name  = userObj.last_name  or ""
    user_info  = await client.get_users(userObj.id)
    is_premium = getattr(user_info, "is_premium", False)
    bio        = userObj.bio if is_premium else (userObj.bio[:70] if userObj.bio else "")

    try:
        photos = [p async for p in client.get_chat_photos(userObj.id)]
        if photos:
            pfp = await client.download_media(photos[0].file_id)
            await client.set_profile_photo(photo=pfp)
    except Exception:
        pass

    await client.update_profile(first_name=first_name, last_name=last_name, bio=bio)
