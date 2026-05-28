import asyncio
import random

from gc import get_objects
from asyncio import sleep
from pyrogram import enums
from pyrogram.raw.functions.messages import DeleteHistory, StartBot
from pyrogram.errors.exceptions import *
from pyrogram.errors.exceptions.not_acceptable_406 import ChannelPrivate

from PyroUbot import *

__MODULE__ = "ʙʀᴏᴀᴅᴄᴀꜱᴛ"
__HELP__ = """
<blockquote><b>
<b>Perintah:</b> <code>{0}ɢɪᴋᴇꜱ</code>

ᴛʏᴘᴇ : ᴀʟʟ , ᴜꜱᴇʀꜱ , ɢʀᴏᴜᴘ

ᴀʟʟ ᴜɴᴛᴜᴋ ꜱᴇᴍᴜᴀ , ᴜꜱᴇʀꜱ ᴜɴᴛᴜᴋ ᴜꜱᴇʀ, ɢʀᴏᴜᴘ ᴜɴᴛᴜᴋ ɢʀᴏᴜᴘ

<b>Perintah:</b> <code>{0}ꜱᴛᴏᴘɢ</code>
    ᴜɴᴛᴜᴋ ᴍᴇɴɢʜᴇɴᴛɪᴋᴀɴ ᴘʀᴏꜱᴇꜱ ɢɪᴋᴇꜱ ʏᴀɴɢ ꜱᴇᴅᴀɴɢ ʙᴇʀʟᴀɴɢꜱᴜɴɢ

<b>Perintah:</b> <code>{0}ʙᴄꜰᴅ</code> ᴏʀ <code>{0}ᴄꜰᴅ</code>
    ᴍᴇɴɢɪʀɪᴍ ᴘᴇꜱᴀɴ ꜱɪᴀʀᴀɴ ꜱᴇᴄᴀʀᴀ ꜰᴏʀᴡᴀʀᴅ (ꜱᴜᴘᴘᴏʀᴛ ᴄʜᴀɴɴᴇʟ)

<b>Perintah:</b> <code>{0}ꜱᴇɴᴅ</code>
    ᴍᴇɴɢɪʀɪᴍ ᴘᴇꜱᴀɴ ᴋᴇ ᴜꜱᴇʀ/ɢʀᴏᴜᴘ/ᴄʜᴀɴɴᴇʟ

<b>Perintah:</b> <code>{0}ᴀᴜᴛᴏʙᴄ</code>
    ᴍᴇɴɢɪʀɪᴍ ᴘᴇꜱᴀɴ ꜱɪᴀʀᴀɴ ꜱᴇᴄᴀʀᴀ ᴏᴛᴏᴍᴀᴛɪꜱ (ꜱᴇʀᴠᴇʀ-ꜱɪᴅᴇ)

ǫᴜᴇʀʏ ᴀᴜᴛᴏʙᴄ:
    | ᴏɴ | ᴏꜰꜰ | ᴛᴇxᴛ | ᴅᴇʟᴀʏ | ʀᴇᴍᴏᴠᴇ | ʟɪꜱᴛ | ʟɪᴍɪᴛ
    (ꜱᴜᴘᴘᴏʀᴛ ʀᴇᴘʟʏ ᴍᴇᴅɪᴀ ꜰᴏᴛᴏ/ꜱᴛɪᴋᴇʀ/ᴠɪᴅᴇᴏ)</b></blockquote>
"""


async def limit_cmd(client, message):

    ggl = await EMO.gagal(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    pong = await EMO.PING(client)
    tion = await EMO.MENTION(client)
    yubot = await EMO.UBOT(client)

    await client.unblock_user("SpamBot")

    bot_info = await client.resolve_peer("SpamBot")

    msg = await message.reply(f"<blockquote>{prs}sebentar ya...</blockquote>")

    response = await client.invoke(
        StartBot(
            bot=bot_info,
            peer=bot_info,
            random_id=client.rnd_id(),
            start_param="start",
        )
    )

    await sleep(1)
    await msg.delete()

    status = await client.get_messages("SpamBot", response.updates[1].message.id + 1) 

    if status and hasattr(status, "text"):
        pjg = len(status.text)
        print(pjg)

        if pjg <= 100:
            if client.me.is_premium:
                text = f"""
<blockquote>{pong} ꜱᴛᴀᴛᴜꜱ ᴀᴋᴜɴ ᴘʀᴇᴍɪᴜᴍ : ᴛʀᴜᴇ
{tion} ʟɪᴍɪᴛ ᴄʜᴇᴄᴋ : ᴀᴋᴜɴ ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ᴅɪʙᴀᴛᴀꜱɪ
{yubot} ᴜʙᴏᴛ : {client.me.mention}</blockquote>
"""
            else:
                text = f"""
<blockquote>ꜱᴛᴀᴛᴜꜱ ᴀᴋᴜɴ : ʙᴇʟɪ ᴘʀᴇᴍ ᴅᴜʟᴜ ʏᴀ
ʟɪᴍɪᴛ ᴄʜᴇᴄᴋ : ᴀᴋᴜɴ ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ᴅɪʙᴀᴛᴀꜱɪ
ᴜʙᴏᴛ : {client.me.mention}</blockquote>
"""
            await client.send_message(message.chat.id, text)
            return await client.invoke(DeleteHistory(peer=bot_info, max_id=0, revoke=True))

        else:
            if client.me.is_premium:
                text = f"""
<blockquote>{pong} ꜱᴛᴀᴛᴜꜱ ᴀᴋᴜɴ ᴘʀᴇᴍɪᴜᴍ : ᴛʀᴜᴇ
{tion} ʟɪᴍɪᴛ ᴄʜᴇᴄᴋ : ᴀᴋᴜɴ ᴀɴᴅᴀ ʙᴇʀᴍᴀꜱᴀʟᴀʜ
{yubot} ᴜʙᴏᴛ : {client.me.mention}</blockquote>
"""
            else:
                text = f"""
<blockquote>ꜱᴛᴀᴛᴜꜱ ᴀᴋᴜɴ : ʙᴇʟɪ ᴘʀᴇᴍ ᴅᴜʟᴜ ʏᴀ
ʟɪᴍɪᴛ ᴄʜᴇᴄᴋ : ᴀᴋᴜɴ ᴀɴᴅᴀ ʙᴇʀᴍᴀꜱᴀʟᴀʜ
ᴜʙᴏᴛ : {client.me.mention}</blockquote>
"""
            await client.send_message(message.chat.id, text)
            return await client.invoke(DeleteHistory(peer=bot_info, max_id=0, revoke=True))
    else:
        print("Status tidak valid atau status.text ga ada")


gcast_progress = []


@PY.UBOT("bc|gikes")
@PY.TOP_CMD
async def gcast_handler(client, message):

    global gcast_progress
    gcast_progress.append(client.me.id)
    
    robot = await EMO.ROBOT(client)
    terompet = await EMO.TEROMPET(client)
    centang = await EMO.CENTANG(client)
    pesan = await EMO.PESAN(client)
    jam = await EMO.JAM(client)
    silang = await EMO.SILANG(client)
    prs = await EMO.PROSES(client)
    ggl = await EMO.gagal(client)
    sks = await EMO.BERHASIL(client)
    
    _msg = f"<blockquote><b>{prs}lagi proses...</b></blockquote>"
    gcs = await message.reply(_msg)    

    command, text = extract_type_and_msg(message)

    if command not in ["group", "users", "all"] or not text:
        if client.me.id in gcast_progress:
            gcast_progress.remove(client.me.id)
        return await gcs.edit(f"<blockquote><code>{message.text.split()[0]}</code> <b>[ᴛʏᴘᴇ] [ᴛᴇxᴛ/ʀᴇᴘʟʏ]</b> {ggl}</blockquote>")
    
    chats = await get_data_id(client, command)
    blacklist = await get_list_from_vars(client.me.id, "BL_ID")

    done = 0
    failed = 0

    for chat_id in chats:

        if client.me.id not in gcast_progress:
            await gcs.edit(f"<blockquote><b>ᴘʀᴏꜱᴇꜱ ɢᴄᴀꜱᴛ ʙᴇʀʜᴀꜱɪʟ ᴅɪ ʙᴀᴛᴀʟᴋᴀɴ !</b> {sks}</blockquote>")
            return
            
        if chat_id in blacklist or chat_id in BLACKLIST_CHAT:
            continue

        try:
            if message.reply_to_message:
                await text.copy(chat_id)
            else:
                await client.send_message(chat_id, text)
            done += 1
            await asyncio.sleep(0.3)

        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                if message.reply_to_message:
                    await text.copy(chat_id)
                else:
                    await client.send_message(chat_id, text)
                done += 1
            except (Exception, ChannelPrivate):
                failed += 1

        except (Exception, ChannelPrivate):
            failed += 1

    if client.me.id in gcast_progress:
        gcast_progress.remove(client.me.id)
        
    await gcs.delete()

    _gcs = f"""
<blockquote>{robot} <b>ʏᴏᴜʀ ʙʀᴏᴀᴅᴄᴀꜱᴛ ʀᴇꜱᴜʟᴛ</b> {terompet}
  {centang} <b>ꜱᴜᴄᴄᴇꜱꜱ: {done}</b>
  {silang} <b>ꜰᴀɪʟᴇᴅ: {failed}</b>
  {robot} <b>ᴛᴀꜱᴋ ɪᴅ: {message.id}</b>
  {pesan} <b>ᴛʏᴘᴇ: {command}</b>
  {jam} <b>ʙʟᴀᴄᴋʟɪꜱᴛ: {len(blacklist)}</b>
<b>ᴍʏ ʙᴏᴛ: @{client.me.username}</b></blockquote>
"""
    return await message.reply(_gcs)


@PY.UBOT("stopg")
@PY.TOP_CMD
async def stopg_handler(client, message):

    sks = await EMO.BERHASIL(client)
    ggl = await EMO.gagal(client)
    global gcast_progress

    if client.me.id in gcast_progress:
        gcast_progress.remove(client.me.id)
        return await message.reply(f"<blockquote><b>ɢᴄᴀꜱᴛ ʙᴇʀʜᴀꜱɪʟ ᴅɪ ᴄᴀɴᴄᴇʟ</b> {sks}</blockquote>")
    else:
        return await message.reply(f"<blockquote><b>{ggl}ᴛɪᴅᴀᴋ ᴀᴅᴀ ɢᴄᴀꜱᴛ !!!</b></blockquote>")


@PY.UBOT("bcfd|cfd")
@PY.TOP_CMD
async def _(client, message):

    import asyncio
    from pyrogram.errors import FloodWait, SlowmodeWait

    robot = await EMO.ROBOT(client)
    terompet = await EMO.TEROMPET(client)
    centang = await EMO.CENTANG(client)
    pesan = await EMO.PESAN(client)
    jam = await EMO.JAM(client)
    silang = await EMO.SILANG(client)
    prs = await EMO.PROSES(client)
    ggl = await EMO.gagal(client)

    _msg = f"<blockquote>{prs}lagi proses...</blockquote>"
    gcs = await message.reply(_msg)

    type_query = get_arg(message) or "all"

    if not message.reply_to_message:
        return await gcs.edit(
            f"<blockquote>{ggl}ᴍᴏʜᴏɴ ʙᴀʟᴀꜱ ᴋᴇ ᴘᴇꜱᴀɴ ʏᴀɴɢ ɪɴɢɪɴ ᴅɪꜰᴏʀᴡᴀʀᴅ</blockquote>"
        )

    chats = []

    if type_query == "group":
        chats = await get_data_id(client, "group")

    elif type_query == "users":
        chats = await get_data_id(client, "users")

    elif type_query in ["ch", "channel"]:
        async for dialog in client.get_dialogs():
            if dialog.chat.type == enums.ChatType.CHANNEL:
                chats.append(dialog.chat.id)

    else:
        async for dialog in client.get_dialogs():
            if dialog.chat.type in (
                enums.ChatType.GROUP,
                enums.ChatType.SUPERGROUP,
                enums.ChatType.PRIVATE,
                enums.ChatType.CHANNEL
            ):
                chats.append(dialog.chat.id)

    blacklist = await get_list_from_vars(client.me.id, "BL_ID")

    done = 0
    failed = 0

    for chat_id in chats:

        if chat_id in blacklist or chat_id in BLACKLIST_CHAT:
            continue

        try:
            await message.reply_to_message.forward(chat_id)
            done += 1

            # Delay aman anti flood
            await asyncio.sleep(2)

        except FloodWait as e:
            await asyncio.sleep(e.value)

            try:
                await message.reply_to_message.forward(chat_id)
                done += 1
                await asyncio.sleep(2)

            except Exception:
                failed += 1

        except SlowmodeWait as e:
            await asyncio.sleep(e.value)

            try:
                await message.reply_to_message.forward(chat_id)
                done += 1
                await asyncio.sleep(2)

            except Exception:
                failed += 1

        except Exception:
            failed += 1
            await asyncio.sleep(1)

    await gcs.delete()

    _gcs = f"""
<blockquote>{robot} <b>ꜰᴏʀᴡᴀʀᴅ ʙʀᴏᴀᴅᴄᴀꜱᴛ ʀᴇꜱᴜʟᴛ</b>
{centang} <b>ꜱᴜᴄᴄᴇꜱꜱ: {done}</b>
{silang} <b>ꜰᴀɪʟᴇᴅ: {failed}</b>
{robot} <b>ᴛᴀꜱᴋ ɪᴅ: {message.id}</b>
{pesan} <b>ᴛʏᴘᴇ: {type_query}</b>
{jam} <b>ʙʟᴀᴄᴋʟɪꜱᴛ: {len(blacklist)}</b>
<b>ᴍʏ ʙᴏᴛ: @{client.me.username}</b>
</blockquote>
"""

    return await message.reply(_gcs)


@PY.BOT("bcast")
@PY.ADMIN
async def _(client, message):

    msg = await message.reply("<blockquote><b>gas, lagi proses...</blockquote></b>\n\n<blockquote><b>ᴍᴏʜᴏɴ ʙᴇʀꜱᴀʙᴀʀ ᴜɴᴛᴜᴋ ᴍᴇɴᴜɴɢɢᴜ ᴘʀᴏꜱᴇꜱ ʙʀᴏᴀᴅᴄᴀꜱᴛ ꜱᴀᴍᴘᴀɪ ꜱᴇʟᴇꜱᴀɪ</blockquote></b>", quote=True)

    send = get_message(message)

    if not send:
        return await msg.edit("ᴍᴏʜᴏɴ ʙᴀʟᴀꜱ ᴀᴛᴀᴜ ᴋᴇᴛɪᴋ ꜱᴇꜱᴜᴀᴛᴜ...")
        
    susers = await get_list_from_vars(client.me.id, "SAVED_USERS")
    done = 0

    for chat_id in susers:
        try:
            if message.reply_to_message:
                await send.forward(chat_id)
            else:
                await client.send_message(chat_id, send)
            done += 1

        except FloodWait as e:
            await asyncio.sleep(e.value)
            if message.reply_to_message:
                await send.forward(chat_id)
            else:
                await client.send_message(chat_id, send)
            done += 1

        except Exception:
            pass

    return await msg.edit(f"<blockquote><b>ᴘᴇꜱᴀɴ ʙʀᴏᴀᴅᴄᴀꜱᴛ ʙᴇʀʜᴀꜱɪʟ ᴛᴇʀᴋɪʀɪᴍ ᴋᴇ {done} ᴜꜱᴇʀ</blockquote></b>\n\n<blockquote><b>`ᴜꜱᴇʀʙᴏᴛ 10ᴋ/ʙᴜʟᴀɴ ʙʏ` @ʏᴏɢᴢᴅᴇᴠ</b></blockquote>")


@PY.UBOT("addbl")
@PY.TOP_CMD
async def _(client, message):

    prs = await EMO.PROSES(client)
    grp = await EMO.BL_GROUP(client)
    ktrn = await EMO.BL_KETERANGAN(client)
    _msg = f"<blockquote>{prs}lagi proses...</blockquote>"

    msg = await message.reply(_msg)

    try:
        chat_id = message.chat.id
        blacklist = await get_list_from_vars(client.me.id, "BL_ID")

        if chat_id in blacklist:
            txt = f"""
<blockquote><b>{grp} ɢʀᴏᴜᴘ: {message.chat.title}</blockquote></b>
<blockquote><b>{ktrn} ᴋᴇᴛ: ꜱᴜᴅᴀʜ ᴀᴅᴀ ᴅᴀʟᴀᴍ ʟɪꜱᴛ ʙʟᴀᴄᴋʟɪꜱᴛ</blockquote></b>
"""
        else:
            await add_to_vars(client.me.id, "BL_ID", chat_id)
            txt = f"""
<blockquote><b>{grp} ɢʀᴏᴜᴘ: {message.chat.title}</blockquote></b>\n<blockquote><b>{ktrn} ᴋᴇᴛ: ꜱᴜᴄᴄᴇꜱꜱ ᴀᴅᴅ ꜰᴏʀ ʙʟᴀᴄᴋʟɪꜱᴛ</blockquote></b>
"""
        return await msg.edit(txt)

    except Exception as error:
        return await msg.edit(str(error))


@PY.UBOT("unbl")
@PY.TOP_CMD
async def _(client, message):

    prs = await EMO.PROSES(client)
    grp = await EMO.BL_GROUP(client)
    ktrn = await EMO.BL_KETERANGAN(client)
    _msg = f"<blockquote>{prs}lagi proses...</blockquote>"

    msg = await message.reply(_msg)

    try:
        chat_id = get_arg(message) or message.chat.id
        blacklist = await get_list_from_vars(client.me.id, "BL_ID")

        if chat_id not in blacklist:
            response = f"""
<blockquote><b>{grp} ɢʀᴏᴜᴘ: {message.chat.title}</blockquote></b>
<blockquote><b>{ktrn} ᴋᴇᴛ: ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴅᴀʟᴀᴍ ʟɪꜱᴛ</b></blockquote>
"""
        else:
            await remove_from_vars(client.me.id, "BL_ID", chat_id)
            response = f"""
<blockquote><b>{grp} ɢʀᴏᴜᴘ: {message.chat.title}</blockquote ></b>
<blockquote><b>{ktrn} ᴋᴇᴛ: ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ʀᴇᴍᴏᴠᴇᴅ ꜰʀᴏᴍ ᴛʜᴇ ʙʟᴀᴄᴋʟɪꜱᴛ</blockquote></b>
"""
        return await msg.edit(response)

    except Exception as error:
        return await msg.edit(str(error))


@PY.UBOT("listbl")
@PY.TOP_CMD
async def _(client, message):

    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ktrng = await EMO.BL_KETERANGAN(client)
    _msg = f"<blockquote>{prs}lagi proses...</blockquote>"
    mzg = await message.reply(_msg)

    blacklist = await get_list_from_vars(client.me.id, "BL_ID")
    total_blacklist = len(blacklist)

    list_res = f"<blockquote>{brhsl} ᴅᴀꜰᴛᴀʀ ʙʟᴀᴄᴋʟɪꜱᴛ\n"

    for chat_id in blacklist:
        try:
            chat = await client.get_chat(chat_id)
            list_res += f" ├ {chat.title} | <code>{chat.id}</code>\n"
        except:
            list_res += f" ├ <code>{chat_id}</code>\n"

    list_res += f"\n{ktrng} ᴛᴏᴛᴀʟ ʙʟᴀᴄᴋʟɪꜱᴛ {total_blacklist}</blockquote>"
    return await mzg.edit(list_res)


@PY.UBOT("rallbl")
@PY.TOP_CMD
async def _(client, message):

    prs = await EMO.PROSES(client)
    ggl = await EMO.gagal(client)
    brhsl = await EMO.BERHASIL(client)
    _msg = f"<blockquote>{prs}lagi proses...</blockquote>"

    msg = await message.reply(_msg)
    blacklists = await get_list_from_vars(client.me.id, "BL_ID")

    if not blacklists:
        return await msg.edit(f"<blockquote>{ggl}ʙʟᴀᴄᴋʟɪꜱᴛ ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴀɴᴅᴀ ᴋᴏꜱᴏɴɢ</blockquote>")

    for chat_id in blacklists:
        await remove_from_vars(client.me.id, "BL_ID", chat_id)

    await msg.edit(f"<blockquote>{brhsl}ꜱᴇᴍᴜᴀ ʙʟᴀᴄᴋʟɪꜱᴛ ʙʀᴏᴀᴅᴄᴀꜱᴛ ʙᴇʀʜᴀꜱɪʟ ᴅɪ ʜᴀᴘᴜꜱ</blockquote>")


@PY.UBOT("send")
@PY.TOP_CMD
async def _(client, message):

    if message.reply_to_message:
        chat_id = (
            message.chat.id if len(message.command) < 2 else message.text.split()[1]
        )
        try:
            if client.me.id != bot.me.id:
                if message.reply_to_message.reply_markup:
                    x = await client.get_inline_bot_results(
                        bot.me.username, f"get_send {id(message)}"
                    )
                    return await client.send_inline_bot_result(
                        chat_id, x.query_id, x.results[0].id
                    )
        except Exception as error:
            return await message.reply(error)
        else:
            try:
                return await message.reply_to_message.copy(chat_id)
            except Exception as t:
                return await message.reply(f"<blockquote>ᴇʀʀᴏʀ: {t}</blockquote>")

    else:
        if len(message.command) < 3:
            return await message.reply("<blockquote>ᴋᴇᴛɪᴋ ʏᴀɴɢ ʙᴇɴᴇʀ</blockquote>")

        chat_id, chat_text = message.text.split(None, 2)[1:]

        try:
            if "_" in chat_id:
                msg_id, to_chat = chat_id.split("_")
                return await client.send_message(
                    to_chat, chat_text, reply_to_message_id=int(msg_id)
                )
            else:
                return await client.send_message(chat_id, chat_text)
        except Exception as t:
            return await message.reply(f"<blockquote>ᴇʀʀᴏʀ: {t}</blockquote>")


@PY.INLINE("^get_send")
async def _(client, inline_query):

    _id = int(inline_query.query.split()[1])
    m = next((obj for obj in get_objects() if id(obj) == _id), None)

    if m:
        await client.answer_inline_query(
            inline_query.id,
            cache_time=0,
            results=[
                InlineQueryResultArticle(
                    title="ɢᴇᴛ ꜱᴇɴᴅ!",
                    reply_markup=m.reply_to_message.reply_markup,
                    input_message_content=InputTextMessageContent(
                        m.reply_to_message.text
                    ),
                )
            ],
        )


# --- [ ʟᴏɢɪᴋᴀ ᴀᴜᴛᴏʙᴄ ꜱᴇʀᴠᴇʀ-ꜱɪᴅᴇ + ᴍᴇᴅɪᴀ ] ---

@PY.UBOT("autobc")
@PY.TOP_CMD
async def _(client, message):

    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    bcs = await EMO.BROADCAST(client)
    mng = await EMO.MENUNGGU(client)
    ggl = await EMO.gagal(client)   
    
    msg = await message.reply(f"<blockquote>{prs}lagi proses...</blockquote>")
    type_query, value = extract_type_and_text(message)

    auto_text_vars = await get_vars(client.me.id, "AUTO_TEXT") or []

    if type_query == "on":
        await set_vars(client.me.id, "AUTOGCAST_ON", True)
        return await msg.edit(f"<blockquote>{brhsl}<b>ᴀᴜᴛᴏ ɢᴄᴀꜱᴛ ᴅɪᴀᴋᴛɪꜰᴋᴀɴ ꜱᴇʀᴠᴇʀ-ꜱɪᴅᴇ!</b>\nᴜʙᴏᴛ ᴀᴋᴀɴ ꜱʜᴀʀᴇ ᴏᴛᴏᴍᴀᴛɪꜱ ᴡᴀʟᴀᴜ ᴀᴘʟɪᴋᴀꜱɪ ᴅɪᴛᴜᴛᴜᴘ.</blockquote>")

    elif type_query == "off":
        await set_vars(client.me.id, "AUTOGCAST_ON", False)
        return await msg.edit(f"<blockquote>{brhsl}ᴀᴜᴛᴏ ɢᴄᴀꜱᴛ ᴅɪɴᴏɴᴀᴋᴛɪꜰᴋᴀɴ</blockquote>")

    elif type_query == "text":

        if message.reply_to_message:
            await set_vars(client.me.id, "AUTO_BC_MEDIA", message.reply_to_message.id)
            await set_vars(client.me.id, "AUTO_BC_CHAT", message.chat.id)
            await set_vars(client.me.id, "AUTO_BC_TYPE", "media")
            return await msg.edit(f"<blockquote>{brhsl}ᴍᴇᴅɪᴀ ʙᴇʀʜᴀꜱɪʟ ᴅɪꜱɪᴍᴘᴀɴ ᴜɴᴛᴜᴋ ᴀᴜᴛᴏʙᴄ!</blockquote>")

        else:
            if not value:
                return await msg.edit(f"<blockquote>{ggl}ɢᴜɴᴀᴋᴀɴ: .ᴀᴜᴛᴏʙᴄ ᴛᴇxᴛ [ᴠᴀʟᴜᴇ] ᴀᴛᴀᴜ ʀᴇᴘʟʏ ᴍᴇᴅɪᴀ</blockquote>")
            auto_text_vars.append(value)
            await set_vars(client.me.id, "AUTO_TEXT", auto_text_vars)
            await set_vars(client.me.id, "AUTO_BC_TYPE", "text")
            return await msg.edit(f"<blockquote>{brhsl}ᴛᴇxᴛ ʙᴇʀʜᴀꜱɪʟ ᴅɪꜱɪᴍᴘᴀɴ</blockquote>")

    elif type_query == "delay":

        if not value:
            return await msg.edit(f"<blockquote>{ggl}ɢᴜɴᴀᴋᴀɴ: .ᴀᴜᴛᴏʙᴄ ᴅᴇʟᴀʏ [ᴍᴇɴɪᴛ]</blockquote>")
        await set_vars(client.me.id, "DELAY_GCAST", value)
        return await msg.edit(f"<blockquote>{brhsl}ᴅᴇʟᴀʏ ʙᴇʀʜᴀꜱɪʟ ᴋᴇ ꜱᴇᴛᴛɪɴɢ {value} ᴍᴇɴɪᴛ</blockquote>")

    elif type_query == "remove":

        if value == "all":
            await set_vars(client.me.id, "AUTO_TEXT", [])
            await set_vars(client.me.id, "AUTO_BC_TYPE", None)
            return await msg.edit(f"<blockquote>{brhsl}ꜱᴇᴍᴜᴀ ᴛᴇxᴛ ʙᴇʀʜᴀꜱɪʟ ᴅɪʜᴀᴘᴜꜱ</blockquote>")
        try:
            idx = int(value) - 1
            auto_text_vars.pop(idx)
            await set_vars(client.me.id, "AUTO_TEXT", auto_text_vars)
            return await msg.edit(f"<blockquote>{brhsl}ᴛᴇxᴛ ᴋᴇ {value} ʙᴇʀʜᴀꜱɪʟ ᴅɪʜᴀᴘᴜꜱ</blockquote>")
        except:
            return await msg.edit("<blockquote>ɪɴᴅᴇx ᴛɪᴅᴀᴋ ᴠᴀʟɪᴅ</blockquote>")

    elif type_query == "list":

        if not auto_text_vars:
            return await msg.edit(f"<blockquote>{ggl}ᴀᴜᴛᴏ ɢᴄᴀꜱᴛ ᴛᴇxᴛ ᴋᴏꜱᴏɴɢ</blockquote>")

        txt = "<blockquote><b>ᴅᴀꜰᴛᴀʀ ᴀᴜᴛᴏ ɢᴄᴀꜱᴛ ᴛᴇxᴛ:</b>\n"
        for num, x in enumerate(auto_text_vars, 1):
            txt += f" {num}. {x}\n"
        return await msg.edit(txt + "</blockquote>")

    else:
        return await msg.edit(f"<blockquote>ǫᴜᴇʀʏ: ᴏɴ, ᴏꜰꜰ, ᴛᴇxᴛ, ᴅᴇʟᴀʏ, ʀᴇᴍᴏᴠᴇ, ʟɪꜱᴛ</blockquote>")


# --- [ ʙᴀᴄᴋɢʀᴏᴜɴᴅ ᴡᴏʀᴋᴇʀ ᴀᴜᴛᴏʙᴄ ] ---

async def startup_autobc():

    while True:

        for x in ubot._ubot:
            try:
                user_id = x.me.id
                is_on = await get_vars(user_id, "AUTOGCAST_ON")

                if is_on:
                    delay = await get_vars(user_id, "DELAY_GCAST") or 1
                    blacklist = await get_list_from_vars(user_id, "BL_ID")
                    bc_type = await get_vars(user_id, "AUTO_BC_TYPE")

                    group_count = 0
                    
                    async for dialog in x.get_dialogs():
                        if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
                            if dialog.chat.id not in blacklist and dialog.chat.id not in BLACKLIST_CHAT:
                                try:
                                    if bc_type == "media":
                                        m_id = await get_vars(user_id, "AUTO_BC_MEDIA")
                                        c_id = await get_vars(user_id, "AUTO_BC_CHAT")
                                        await x.copy_message(dialog.chat.id, c_id, m_id)
                                    else:
                                        t_list = await get_vars(user_id, "AUTO_TEXT")
                                        if t_list:
                                            await x.send_message(dialog.chat.id, random.choice(t_list))
                                    
                                    group_count += 1
                                    await asyncio.sleep(1.5)

                                except FloodWait as e:
                                    await asyncio.sleep(e.value)
                                except:
                                    continue

                    try:
                        await x.send_message("me", f"<blockquote>⌬ ᴀᴜᴛᴏʙᴄ ꜱᴇʀᴠᴇʀ ᴅᴏɴᴇ!\n⟶ ʙᴇʀʜᴀꜱɪʟ ᴋᴇ {group_count} ɢʀᴏᴜᴘ.</blockquote>")
                    except:
                        pass

                    await asyncio.sleep(int(60 * int(delay)))

            except Exception:
                pass

        await asyncio.sleep(20)


# JALANKAN BACKGROUND TASK
asyncio.create_task(startup_autobc())


@PY.BOT("bcubot")
@PY.ADMIN
async def broadcast_bot(client, message):

    msg = await message.reply("<blockquote><b>lagi diproses...</b></blockquote>", quote=True)
    done = 0

    if not message.reply_to_message:
        return await msg.edit("ᴍᴏʜᴏɴ ʙᴀʟᴀꜱ ᴘᴇꜱᴀɴ!")

    for x in ubot._ubot:
        try:
            await x.unblock_user(bot.me.username)
            await message.reply_to_message.forward(x.me.id)
            done += 1
        except:
            pass

    return await msg.edit(f"<blockquote>⌬ ʙᴇʀʜᴀꜱɪʟ ᴍᴇɴɢɪʀɪᴍ ᴘᴇꜱᴀɴ ᴋᴇ {done} ᴜʙᴏᴛ</blockquote>")