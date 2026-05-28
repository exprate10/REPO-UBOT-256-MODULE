from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytz import timezone
from PyroUbot import *

__MODULE__ = "ᴅʙ ᴄᴏɴᴛʀᴏʟ"
__HELP__ = """
<blockquote><b>ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴅʙ ᴄᴏɴᴛʀᴏʟ</b></blockquote>

<blockquote><b>ᴘᴇʀɪɴᴛᴀʜ : <code>{0}ᴛɪᴍᴇ</code>
    ᴜɴᴛᴜᴋ ᴍᴇɴᴀᴍʙᴀʜ - ᴍᴇɴɢᴜʀᴀɴɢɪ ᴍᴀsᴀ ᴀᴋᴛɪғ ᴜsᴇʀ</b></blockquote>

<blockquote><b>ᴘᴇʀɪɴᴛᴀʜ : <code>{0}ᴄᴇᴋ</code>
    ᴜɴᴛᴜᴋ ᴍᴇʟɪʜᴀᴛ ᴍᴀsᴀ ᴀᴋᴛɪғ ᴜsᴇʀ</b></blockquote>

<blockquote><b>ᴘᴇʀɪɴᴛᴀʜ : <code>{0}ᴀᴅᴅᴀᴅᴍɪɴ</code> - <code>{0}ᴜɴᴀᴅᴍɪɴ</code> - <code>{0}ɢᴇᴛᴀᴅᴍɪɴ</code></b></blockquote>

<blockquote><b>ᴘᴇʀɪɴᴛᴀʜ : <code>{0}sᴇʟᴇs</code> - <code>{0}ᴜɴsᴇʟᴇs</code> - <code>{0}ɢᴇᴛsᴇʟᴇs</code></b></blockquote>
"""

@PY.BOT("prem")
@PY.SELLER
async def _(client, message):
    user_id, get_bulan = await extract_user_and_reason(message)
    msg = await message.reply("<b>ᴍᴇᴍᴘʀᴏsᴇs...</b>")
    if not user_id:
        return await msg.edit(f"<b>{message.text} ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ - ʙᴜʟᴀɴ</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)
    if not get_bulan:
        get_bulan = 1

    prem_users = await get_list_from_vars(client.me.id, "PREM_USERS")

    if user.id in prem_users:
        return await msg.edit(f"""
<blockquote><b>ɴᴀᴍᴇ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>ɪᴅ: {user.id}</b>
<b>ᴋᴇᴛᴇʀᴀɴɢᴀɴ: sᴜᴅᴀʜ ᴘʀᴇᴍɪᴜᴍ</b>
<b>ᴇxᴘɪʀᴇᴅ: {get_bulan} ʙᴜʟᴀɴ</b></blockquote>
"""
        )

    try:
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=int(get_bulan))
        await set_expired_date(user_id, expired)
        await add_to_vars(client.me.id, "PREM_USERS", user.id)
        await msg.edit(f"""
<blockquote><b>ɴᴀᴍᴇ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>ɪᴅ: {user.id}</b>
<b>ᴇxᴘɪʀᴇᴅ: {get_bulan} ʙᴜʟᴀɴ</b>
<b>sɪʟᴀʜᴋᴀɴ ʙᴜᴋᴀ @{client.me.username} ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ</b></blockquote>

<blockquote>ᴄᴀʀᴀ ʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ :
- sɪʟᴀʜᴋᴀɴ /sᴛᴀʀᴛ ᴅᴜʟᴜ ʙᴏᴛ @UbotZexcOfficial_bot
- ᴋᴀʟᴀᴜ sᴜᴅᴀʜ sᴛᴀʀᴛ ʙᴏᴛ ᴀʙɪsᴛᴜ ᴘᴇɴᴄᴇᴛ ᴛᴏᴍʙᴏʟ ʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ 
- ɴᴀʜ ɴᴀɴᴛɪ ᴀᴅᴀ ᴀʀᴀʜᴀɴ ᴅᴀʀɪ ʙᴏᴛ ɴʏᴀ ɪᴛᴜ ɪᴋᴜᴛɪɴ</blockquote>
<blockquote><b>ɴᴏᴛᴇ : ᴊᴀɴɢᴀɴ ʟᴜᴘᴀ ʙᴀᴄᴀ ᴀʀᴀʜᴀɴ ᴅᴀʀɪ ʙᴏᴛ ɴʏᴀ</b></blockquote>
"""
        )
        return await bot.send_message(
            OWNER_ID,
            f"🆔 ɪᴅ-sᴇʟʟᴇʀ: {message.from_user.id}\n\n🆔 ɪᴅ-ᴄᴜsᴛᴏᴍᴇʀ: {user_id}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔱 sᴇʟʟᴇʀ",
                            callback_data=f"profil {message.from_user.id}",
                        ),
                        InlineKeyboardButton(
                            "ᴄᴜsᴛᴏᴍᴇʀ ⚜️", callback_data=f"profil {user_id}"
                        ),
                    ],
                ]
            ),
        )
    except Exception as error:
        return await msg.edit(error)


@PY.BOT("unprem")
@PY.SELLER
async def _(client, message):
    msg = await message.reply("<b>sᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏsᴇs...</b>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b>{message.text} ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ</b>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    prem_users = await get_list_from_vars(client.me.id, "PREM_USERS")

    if user.id not in prem_users:
        return await msg.edit(f"""
<blockquote><b>ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>
<b>ɴᴀᴍᴀ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>ɪᴅ: {user.id}</b>
<b>ᴋᴇᴛᴇʀᴀɴɢᴀɴ: ᴛɪᴅᴀᴋ ᴅᴀʟᴀᴍ ᴅᴀғᴛᴀʀ</b></blockquote>
"""
        )
    try:
        await remove_from_vars(client.me.id, "PREM_USERS", user.id)
        await rem_expired_date(user_id)
        return await msg.edit(f"""
<blockquote><b>ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>
<b>ɴᴀᴍᴀ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>ɪᴅ: {user.id}</b>
<b>ᴋᴇᴛᴇʀᴀɴɢᴀɴ: ᴜɴᴘʀᴇᴍɪᴜᴍ sᴜᴋsᴇs</b></blockquote>
"""
        )
    except Exception as error:
        return await msg.edit(error)
        

@PY.BOT("getprem")
@PY.SELLER
async def _(client, message):
    text = ""
    count = 0
    prem = await get_list_from_vars(client.me.id, "PREM_USERS")

    for user_id in prem:
        try:
            user = await bot.get_users(user_id)
            count += 1
            userlist = f"• {count}: <a href=tg://user?id={user.id}>{user.first_name} {user.last_name or ''}</a> > <code>{user.id}</code>"
            text += f"<blockquote><b>{userlist}</b></blockquote>"
        except Exception:
            continue
    if not text:
        await message.reply_text("<blockquote><b>ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴘᴇɴɢɢᴜɴᴀ ʏᴀɴɢ ᴅɪᴛᴇᴍᴜᴋᴀɴ</b></blockquote>")
    else:
        await message.reply_text(f"<b>📋 ᴅᴀғᴛᴀʀ ᴘʀᴇᴍɪᴜᴍ:</b>\n\n{text}")


@PY.BOT("seles")
@PY.ADMIN
async def _(client, message):
    msg = await message.reply("<b>sᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏsᴇs...</b>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b>{message.text} ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ</b>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    sudo_users = await get_list_from_vars(client.me.id, "SELER_USERS")

    if user.id in sudo_users:
        return await msg.edit(f"""
<blockquote><b>ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>
<b>ɴᴀᴍᴀ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>ɪᴅ: {user.id}</b>
<b>ᴋᴇᴛᴇʀᴀɴɢᴀɴ: sᴜᴅᴀʜ sᴇʟʟᴇʀ</b></blockquote>
"""
        )

    try:
        await add_to_vars(client.me.id, "SELER_USERS", user.id)
        return await msg.edit(f"""
<blockquote><b>ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>
<b>ɴᴀᴍᴀ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>ɪᴅ: {user.id}</b>
<b>ᴋᴇᴛᴇʀᴀɴɢᴀɴ: sᴜᴋsᴇs ᴊᴀᴅɪ sᴇʟʟᴇʀ</b></blockquote>
"""
        )
    except Exception as error:
        return await msg.edit(error)


@PY.BOT("unseles")
@PY.ADMIN
async def _(client, message):
    msg = await message.reply("<b>sᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏsᴇs...</b>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b>{message.text} ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ</b>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    seles_users = await get_list_from_vars(client.me.id, "SELER_USERS")

    if user.id not in seles_users:
        return await msg.edit(f"""
<blockquote><b>ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>
<b>ɴᴀᴍᴀ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>ɪᴅ: {user.id}</b>
<b>ᴋᴇᴛᴇʀᴀɴɢᴀɴ: ᴛɪᴅᴀᴋ ᴅᴀʟᴀᴍ ᴅᴀғᴛᴀʀ</b></blockquote>
"""
        )

    try:
        await remove_from_vars(client.me.id, "SELER_USERS", user.id)
        return await msg.edit(f"""
<blockquote><b>ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>
<b>ɴᴀᴍᴀ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>ɪᴅ: {user.id}</b>
<b>ᴋᴇᴛᴇʀᴀɴɢᴀɴ: ᴜɴsᴇʟʟᴇʀ sᴜᴋsᴇs</b></blockquote>
"""
        )
    except Exception as error:
        return await msg.edit(error)


@PY.BOT("getseles")
@PY.ADMIN
async def _(client, message):
    Sh = await message.reply("<b>sᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏsᴇs...</b>")
    seles_users = await get_list_from_vars(client.me.id, "SELER_USERS")

    if not seles_users:
        return await Sh.edit("<blockquote><b>ᴅᴀғᴛᴀʀ sᴇʟʟᴇʀ ᴋᴏsᴏɴɢ</b></blockquote>")

    seles_list = []
    for user_id in seles_users:
        try:
            user = await client.get_users(int(user_id))
            seles_list.append(
                f"<blockquote>👤 [{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | <code>{user.id}</code></blockquote>"
            )
        except:
            continue

    if seles_list:
        response = (
            "<b>📋 ᴅᴀғᴛᴀʀ sᴇʟʟᴇʀ:</b>\n\n"
            + "\n".join(seles_list)
            + f"\n\n<blockquote>⚜️ ᴛᴏᴛᴀʟ sᴇʟʟᴇʀ: {len(seles_list)}</blockquote>"
        )
        return await Sh.edit(response)
    else:
        return await Sh.edit("<blockquote><b>ᴛɪᴅᴀᴋ ᴅᴀᴘᴀᴛ ᴍᴇɴɢᴀᴍʙɪʟ ᴅᴀғᴛᴀʀ sᴇʟʟᴇʀ</b></blockquote>")


@PY.BOT("time")
@PY.SELLER
async def _(client, message):
    Tm = await message.reply("<b>ᴘʀᴏᴄᴇssɪɴɢ . . .</b>")
    bajingan = message.command
    if len(bajingan) != 3:
        return await Tm.edit(f"<blockquote><b>ᴍᴏʜᴏɴ ɢᴜɴᴀᴋᴀɴ /sᴇᴛ_ᴛɪᴍᴇ ᴜsᴇʀ_ɪᴅ ʜᴀʀɪ</b></blockquote>")
    user_id = int(bajingan[1])
    get_day = int(bajingan[2])
    try:
        get_id = (await client.get_users(user_id)).id
        user = await client.get_users(user_id)
    except Exception as error:
        return await Tm.edit(error)
    if not get_day:
        get_day = 30
    now = datetime.now(timezone("Asia/Jakarta"))
    expire_date = now + timedelta(days=int(get_day))
    await set_expired_date(user_id, expire_date)
    await Tm.edit(f"""
<blockquote><b>ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>
<b>ɴᴀᴍᴀ:</b> {user.mention}
<b>ɪᴅ:</b> {get_id}
<b>ᴀᴋᴛɪғᴋᴀɴ_sᴇʟᴀᴍᴀ:</b> {get_day} ʜᴀʀɪ</blockquote>
"""
    )


@PY.BOT("cek")
@PY.SELLER
async def _(client, message):
    Sh = await message.reply("<b>ᴘʀᴏᴄᴇssɪɴɢ . . .</b>")
    user_id = await extract_user(message)
    if not user_id:
        return await Sh.edit("<blockquote><b>ᴘᴇɴɢɢᴜɴᴀ ᴛɪᴅᴀᴋ ᴛᴇᴍᴜᴋᴀɴ</b></blockquote>")
    try:
        get_exp = await get_expired_date(user_id)
        sh = await client.get_users(user_id)
    except Exception as error:
        return await Sh.edit(error)
    if get_exp is None:
        await Sh.edit(f"""
<blockquote><b>ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>
<b>ɴᴀᴍᴀ :</b> {sh.mention}
<b>ᴘʟᴀɴ : ɴᴏɴᴇ</b>
<b>ɪᴅ :</b> <code>{user_id}</code>
<b>ᴘʀᴇғɪx : .</b>
<b>ᴇxᴘɪʀᴇᴅ : ɴᴏɴᴀᴋᴛɪғ</b></blockquote>
""")
    else:
        SH = await ubot.get_prefix(user_id)
        exp = get_exp.strftime("%d-%m-%Y")
        if user_id in await get_list_from_vars(client.me.id, "ULTRA_PREM"):
            status = "sᴜᴘᴇʀᴜʟᴛʀᴀ"
        else:
            status = "ᴘʀᴇᴍɪᴜᴍ"
        await Sh.edit(f"""
<blockquote><b>ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>
<b>ɴᴀᴍᴀ :</b> {sh.mention}
<b>ᴘʟᴀɴ :</b> {status}
<b>ɪᴅ :</b> <code>{user_id}</code>
<b>ᴘʀᴇғɪx : {' '.join(SH)}</b>
<b>ᴇxᴘɪʀᴇᴅ : {exp}</b></blockquote>
"""
        )


@PY.BOT("admin")
@PY.OWNER
async def _(client, message):
    msg = await message.reply("<b>sᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏsᴇs...</b>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b>{message.text} ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ</b>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    admin_users = await get_list_from_vars(client.me.id, "ADMIN_USERS")

    if user.id in admin_users:
        return await msg.edit(f"""
<blockquote><b>💬 ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>
<b>ɴᴀᴍᴀ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>ɪᴅ: {user.id}</b>
<b>ᴋᴇᴛᴇʀᴀɴɢᴀɴ: sᴜᴅᴀʜ ᴅᴀʟᴀᴍ ᴅᴀғᴛᴀʀ</b></blockquote>
"""
        )

    try:
        await add_to_vars(client.me.id, "ADMIN_USERS", user.id)
        return await msg.edit(f"""
<blockquote><b>💬 ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>
<b>ɴᴀᴍᴀ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>ɪᴅ: {user.id}</b>
<b>ᴋᴇᴛᴇʀᴀɴɢᴀɴ: sᴜᴋsᴇs ᴊᴀᴅɪ ᴀᴅᴍɪɴ</b></blockquote>
"""
        )
    except Exception as error:
        return await msg.edit(error)


@PY.BOT("unadmin")
@PY.OWNER
async def _(client, message):
    msg = await message.reply("<b>sᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏsᴇs...</b>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b>{message.text} ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ</b>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    admin_users = await get_list_from_vars(client.me.id, "ADMIN_USERS")

    if user.id not in admin_users:
        return await msg.edit(f"""
<blockquote><b>💬 ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>
<b>ɴᴀᴍᴀ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>ɪᴅ: {user.id}</b>
<b>ᴋᴇᴛᴇʀᴀɴɢᴀɴ: ᴛɪᴅᴀᴋ ᴅᴀʟᴀᴍ ᴅᴀғᴛᴀʀ</b></blockquote>
"""
        )

    try:
        await remove_from_vars(client.me.id, "ADMIN_USERS", user.id)
        return await msg.edit(f"""
<blockquote><b>💬 ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>
<b>ɴᴀᴍᴀ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>ɪᴅ: {user.id}</b>
<b>ᴋᴇᴛᴇʀᴀɴɢᴀɴ: ᴜɴᴀᴅᴍɪɴ sᴜᴋsᴇs</b></blockquote>
"""
        )
    except Exception as error:
        return await msg.edit(error)


@PY.BOT("getadmin")
@PY.OWNER
async def _(client, message):
    Sh = await message.reply("<b>sᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏsᴇs...</b>")
    admin_users = await get_list_from_vars(client.me.id, "ADMIN_USERS")

    if not admin_users:
        return await Sh.edit("<blockquote><b>ᴅᴀғᴛᴀʀ ᴀᴅᴍɪɴ ᴋᴏsᴏɴɢ</b></blockquote>")

    admin_list = []
    for user_id in admin_users:
        try:
            user = await client.get_users(int(user_id))
            admin_list.append(
                f"<blockquote>👤 [{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | <code>{user.id}</code></blockquote>"
            )
        except:
            continue

    if admin_list:
        response = (
            "<b>📋 ᴅᴀғᴛᴀʀ ᴀᴅᴍɪɴ:</b>\n\n"
            + "\n".join(admin_list)
            + f"\n\n<blockquote>⚜️ ᴛᴏᴛᴀʟ ᴀᴅᴍɪɴ: {len(admin_list)}</blockquote>"
        )
        return await Sh.edit(response)
    else:
        return await Sh.edit("<blockquote><b>ᴛɪᴅᴀᴋ ᴅᴀᴘᴀᴛ ᴍᴇɴɢᴀᴍʙɪʟ ᴅᴀғᴛᴀʀ ᴀᴅᴍɪɴ</b></blockquote>")

@PY.BOT("superultra")
@PY.SELLER
async def _(client, message):
    user_id, get_bulan = await extract_user_and_reason(message)
    msg = await message.reply("<b>ᴍᴇᴍᴘʀᴏsᴇs...</b>")
    if not user_id:
        return await msg.edit(f"<b>{message.text} ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)
    if not get_bulan:
        get_bulan = 1

    prem_users = await get_list_from_vars(client.me.id, "ULTRA_PREM")

    if user.id in prem_users:
        return await msg.edit(f"""
<blockquote><b>ɴᴀᴍᴇ:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
<b>ɪᴅ:</b> <code>{user.id}</code>
<b>ᴋᴇᴛᴇʀᴀɴɢᴀɴ: sᴜᴅᴀʜ</b> <code>[sᴜᴘᴇʀᴜʟᴛʀᴀ]</code>
<b>ᴇxᴘɪʀᴇᴅ:</b> <code>{get_bulan}</code> <b>ʙᴜʟᴀɴ</b></blockquote>
"""
        )

    try:
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=int(get_bulan))
        await set_expired_date(user_id, expired)
        await add_to_vars(client.me.id, "ULTRA_PREM", user.id)
        await msg.edit(f"""
<blockquote><b>ɴᴀᴍᴇ:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
<b>ɪᴅ:</b> <code>{user.id}</code>
<b>ᴇxᴘɪʀᴇᴅ:</b> <code>{get_bulan}</code> <b>ʙᴜʟᴀɴ</b>
<b>sɪʟᴀʜᴋᴀɴ ʙᴜᴋᴀ</b> @{client.me.username} <b>ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ</b>
<b>sᴛᴀᴛᴜs : </b><code>[sᴜᴘᴇʀᴜʟᴛʀᴀ]</code></blockquote>
"""
        )
        return await bot.send_message(
            OWNER_ID,
            f"🆔 ɪᴅ-sᴇʟʟᴇʀ: {message.from_user.id}\n\n🆔 ɪᴅ-ᴄᴜsᴛᴏᴍᴇʀ: {user_id}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔱 sᴇʟʟᴇʀ",
                            callback_data=f"profil {message.from_user.id}",
                        ),
                        InlineKeyboardButton(
                            "ᴄᴜsᴛᴏᴍᴇʀ ⚜️", callback_data=f"profil {user_id}"
                        ),
                    ],
                ]
            ),
        )
    except Exception as error:
        return await msg.edit(error)

@PY.BOT("rmultra")
@PY.SELLER
async def _(client, message):
    msg = await message.reply("<b>sᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏsᴇs...</b>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b>{message.text} ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ</b>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    prem_users = await get_list_from_vars(client.me.id, "ULTRA_PREM")

    if user.id not in prem_users:
        return await msg.edit(f"""
<blockquote><b>ɴᴀᴍᴇ:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
<b>ɪᴅ:</b> <code>{user.id}</code>
<b>ᴋᴇᴛᴇʀᴀɴɢᴀɴ: ᴛɪᴅᴀᴋ ᴅᴀʟᴀᴍ ᴅᴀғᴛᴀʀ</b></blockquote>
"""
        )
    try:
        await remove_from_vars(client.me.id, "ULTRA_PREM", user.id)
        await rem_expired_date(user_id)
        return await msg.edit(f"""
<blockquote><b>ɴᴀᴍᴇ:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
<b>ɪᴅ:</b> <code>{user.id}</code>
<b>ᴋᴇᴛᴇʀᴀɴɢᴀɴ: ɴᴏɴᴇ sᴜᴘᴇʀᴜʟᴛʀᴀ</b></blockquote>
"""
        )
    except Exception as error:
        return await msg.edit(error)
        

@PY.BOT("getultra")
@PY.SELLER
async def _(client, message):
    prem = await get_list_from_vars(client.me.id, "ULTRA_PREM")
    ultra_list = []

    for user_id in prem:
        try:
            user = await client.get_users(user_id)
            ultra_list.append(
                f"<blockquote>👤 [{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | <code>{user.id}</code></blockquote>"
            )
        except:
            continue

    if ultra_list:
        response = (
            "<b>📋 ᴅᴀғᴛᴀʀ sᴜᴘᴇʀᴜʟᴛʀᴀ:</b>\n\n"
            + "\n".join(ultra_list)
            + f"\n\n<blockquote>⚜️ ᴛᴏᴛᴀʟ sᴜᴘᴇʀᴜʟᴛʀᴀ: {len(ultra_list)}</blockquote>"
        )
        return await message.reply(response)
    else:
        return await message.reply("<blockquote><b>ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴘᴇɴɢɢᴜɴᴀ sᴜᴘᴇʀᴜʟᴛʀᴀ sᴀᴀᴛ ɪɴɪ</b></blockquote>")
        
