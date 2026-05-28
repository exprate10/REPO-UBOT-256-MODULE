import asyncio
import aiohttp
import uuid
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytz import timezone
from PyroUbot import *
from PyroUbot.config import PAKASIR_API_KEY, PAKASIR_MERCHANT_ID, LOGS_MAKER_UBOT

__MODULE__ = "ᴘᴀʏᴍᴇɴᴛ"
__HELP__ = """
<blockquote><b>💳 PAYMENT — RANZ PEDIA</b>

Sistem pembayaran otomatis via QRIS Pakasir.
Bot langsung konfirmasi begitu bayaran masuk!</blockquote>
"""

ROLE_HARGA = {
    "member": {"1": 2000, "0": 3000},
    "seles":  {"1": 4000, "0": 5000},
    "admin":  {"1": 10000, "0": 15000},
}

ROLE_LABEL = {
    "member": "👤 Member",
    "seles":  "💼 Seles",
    "admin":  "⚙️ Admin",
}

DURASI_LABEL = {
    "1": "📅 1 Bulan",
    "0": "♾️ Permanen",
}

pending_payments = {}


async def pakasir_create_invoice(amount: int, order_id: str, description: str) -> dict:
    url = "https://api.pakasir.com/transaction/create"
    headers = {
        "Authorization": f"Bearer {PAKASIR_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "merchant_id": PAKASIR_MERCHANT_ID,
        "order_id": order_id,
        "amount": amount,
        "description": description,
        "payment_method": "qris",
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                return await resp.json()
    except Exception as e:
        return {"error": str(e)}


async def pakasir_check_status(order_id: str) -> dict:
    url = f"https://api.pakasir.com/transaction/status/{order_id}"
    headers = {"Authorization": f"Bearer {PAKASIR_API_KEY}"}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                return await resp.json()
    except Exception as e:
        return {"error": str(e)}


async def get_user_current_role(user_id: int, bot_id: int) -> str:
    admin_list = await get_list_from_vars(bot_id, "ADMIN_USERS")
    seles_list = await get_list_from_vars(bot_id, "SELER_USERS")
    prem_list = await get_list_from_vars(bot_id, "PREM_USERS")
    if user_id in admin_list:
        return "admin"
    elif user_id in seles_list:
        return "seles"
    elif user_id in prem_list:
        return "member"
    return "none"


async def proses_prem_user(user_id: int, role: str, durasi: str, bot_client):
    bot_id = bot_client.me.id

    prem_list = await get_list_from_vars(bot_id, "PREM_USERS")
    if user_id not in prem_list:
        await add_to_vars(bot_id, "PREM_USERS", user_id)

    if role in ("seles", "admin"):
        seles_list = await get_list_from_vars(bot_id, "SELER_USERS")
        if user_id not in seles_list:
            await add_to_vars(bot_id, "SELER_USERS", user_id)

    if role == "admin":
        admin_list = await get_list_from_vars(bot_id, "ADMIN_USERS")
        if user_id not in admin_list:
            await add_to_vars(bot_id, "ADMIN_USERS", user_id)

    now = datetime.now(timezone("Asia/Jakarta"))
    if durasi == "1":
        expired = now + relativedelta(months=1)
    else:
        expired = now + relativedelta(years=100)
    await set_expired_date(user_id, expired)


async def kirim_notif_order(user_id: int, username: str, role: str, durasi: str, order_id: str):
    waktu = datetime.now(timezone("Asia/Jakarta")).strftime("%d-%m-%Y %H:%M:%S")
    label_role = ROLE_LABEL.get(role, role.upper())
    label_durasi = DURASI_LABEL.get(durasi, durasi)
    harga = ROLE_HARGA.get(role, {}).get(durasi, 0)

    text = (
        f"<blockquote><b>✅ ORDER USERBOT SUKSES!</b>\n\n"
        f"<b>🛍️ Detail Order:</b>\n"
        f"<b>├ 👤 User:</b> <a href='tg://user?id={user_id}'>{username}</a>\n"
        f"<b>├ 🆔 User ID:</b> <code>{user_id}</code>\n"
        f"<b>├ 📦 Order ID:</b> <code>{order_id}</code>\n"
        f"<b>├ 🎫 Role:</b> {label_role}\n"
        f"<b>├ 📆 Durasi:</b> {label_durasi}\n"
        f"<b>├ 💰 Nominal:</b> Rp {harga:,}\n"
        f"<b>└ ⏰ Waktu:</b> {waktu}\n\n"
        f"<b>🎉 User berhasil aktifkan userbot!</b></blockquote>"
    )
    try:
        await bot.send_message(LOGS_MAKER_UBOT, text)
    except Exception as e:
        print(f"[ERROR] Gagal kirim notif order: {e}")



@PY.CALLBACK("bahan")
async def pilih_role_callback(client, callback_query):
    user_id = callback_query.from_user.id

    if user_id in ubot._get_my_id:
        btns = [
            [InlineKeyboardButton("🔄 Restart Userbot", callback_data="ress_ubot")],
            [InlineKeyboardButton("⬅️ Kembali", callback_data=f"home {user_id}")],
        ]
        return await callback_query.edit_message_text(
            "<blockquote><b>✅ Kamu udah punya userbot aktif!</b>\n\n"
            "Kalo ubotnya ga respon, coba restart dulu ya.</blockquote>",
            reply_markup=InlineKeyboardMarkup(btns),
        )

    if len(ubot._ubot) + 1 > MAX_BOT:
        return await callback_query.edit_message_text(
            f"<blockquote><b>❌ Slot userbot penuh!</b>\n\n"
            f"<b>Kapasitas:</b> {len(ubot._ubot)} slot\n\n"
            f"Hubungi <a href='tg://openmessage?user_id={OWNER_ID}'>Owner</a> dulu ya!</blockquote>",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data=f"home {user_id}")]]),
        )

    text = (
        "<blockquote><b>🎫 Pilih Role Userbot</b>\n\n"
        "<b>👤 Member</b> — akses fitur standar\n"
        "<b>💼 Seles</b> — akses + bisa jual userbot\n"
        "<b>⚙️ Admin</b> — akses penuh semua fitur\n\n"
        "<b>Pilih role yang kamu mau:</b></blockquote>"
    )
    from PyroUbot.core.helpers.inline import BTN
    return await callback_query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(BTN.ROLE_PICKER(user_id)),
    )


@PY.CALLBACK("^role_pick")
async def role_pick_callback(client, callback_query):
    data = callback_query.data.split()
    role = data[1]
    user_id = int(data[2])

    if callback_query.from_user.id != user_id:
        return await callback_query.answer("Eh, ini bukan buat kamu!", show_alert=True)

    from PyroUbot.core.helpers.inline import BTN
    label_role = ROLE_LABEL.get(role, role.upper())
    harga_1 = ROLE_HARGA[role]["1"]
    harga_0 = ROLE_HARGA[role]["0"]

    text = (
        f"<blockquote><b>✅ Role dipilih: {label_role}</b>\n\n"
        f"<b>Sekarang pilih durasi:</b>\n"
        f"<b>📅 1 Bulan</b> — Rp {harga_1:,}\n"
        f"<b>♾️ Permanen</b> — Rp {harga_0:,}</blockquote>"
    )
    return await callback_query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(BTN.DURASI_PICKER(role, user_id)),
    )


@PY.CALLBACK("^durasi_pick")
async def durasi_pick_callback(client, callback_query):
    data = callback_query.data.split()
    role = data[1]
    durasi = data[2]
    user_id = int(data[3])

    if callback_query.from_user.id != user_id:
        return await callback_query.answer("Bukan buat kamu ini!", show_alert=True)

    label_role = ROLE_LABEL.get(role, role.upper())
    label_durasi = DURASI_LABEL.get(durasi, durasi)
    harga = ROLE_HARGA.get(role, {}).get(durasi, 0)

    from PyroUbot.core.helpers.inline import BTN
    text = (
        f"<blockquote><b>📋 Ringkasan Order</b>\n\n"
        f"<b>🎫 Role:</b> {label_role}\n"
        f"<b>📆 Durasi:</b> {label_durasi}\n"
        f"<b>💰 Harga:</b> Rp {harga:,}\n\n"
        f"<b>Klik Bayar Sekarang buat lanjut ke QRIS!</b></blockquote>"
    )
    return await callback_query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(BTN.KONFIRMASI_BAYAR(role, durasi, user_id)),
    )



@PY.CALLBACK("^pakasir_pay")
async def pakasir_pay_callback(client, callback_query):
    data = callback_query.data.split()
    role = data[1]
    durasi = data[2]
    user_id = int(data[3])

    if callback_query.from_user.id != user_id:
        return await callback_query.answer("Eh ini bukan order kamu!", show_alert=True)

    label_role = ROLE_LABEL.get(role, role.upper())
    label_durasi = DURASI_LABEL.get(durasi, durasi)
    harga = ROLE_HARGA.get(role, {}).get(durasi, 0)
    order_id = f"RANZPEDIA-{user_id}-{uuid.uuid4().hex[:8].upper()}"

    await callback_query.edit_message_text(
        "<blockquote><b>⏳ Lagi bikin QRIS kamu...</b>\n\nSabar ya, sebentar lagi!</blockquote>"
    )

    result = await pakasir_create_invoice(harga, order_id, f"Beli Userbot {label_role} {label_durasi}")

    if "error" in result or result.get("status") not in ("success", "created", True, "pending", 200):
        qris_url = None
        qris_img = None
    else:
        qris_url = result.get("data", {}).get("qr_url") or result.get("qr_url")
        qris_img = result.get("data", {}).get("qr_image") or result.get("qr_image")

    pending_payments[order_id] = {
        "user_id": user_id,
        "role": role,
        "durasi": durasi,
        "harga": harga,
        "status": "pending",
    }

    if qris_img or qris_url:
        caption = (
            f"<blockquote><b>💳 QRIS Pembayaran</b>\n\n"
            f"<b>🎫 Role:</b> {label_role}\n"
            f"<b>📆 Durasi:</b> {label_durasi}\n"
            f"<b>💰 Total:</b> Rp {harga:,}\n"
            f"<b>🆔 Order ID:</b> <code>{order_id}</code>\n\n"
            f"<b>Scan QRIS di atas lewat aplikasi e-wallet / bank kamu!</b>\n"
            f"<b>Bot otomatis konfirmasi begitu bayaran masuk 🙏</b></blockquote>"
        )
        try:
            await callback_query.message.delete()
        except Exception:
            pass
        try:
            if qris_img:
                await bot.send_photo(user_id, photo=qris_img, caption=caption)
            else:
                await bot.send_photo(user_id, photo=qris_url, caption=caption)
        except Exception:
            await bot.send_message(user_id, caption + f"\n\n<b>Link QRIS:</b> {qris_url or qris_img}")
    else:
        await callback_query.edit_message_text(
            f"<blockquote><b>💳 Silakan Transfer Manual</b>\n\n"
            f"<b>🎫 Role:</b> {label_role}\n"
            f"<b>📆 Durasi:</b> {label_durasi}\n"
            f"<b>💰 Total:</b> Rp {harga:,}\n"
            f"<b>🆔 Order ID:</b> <code>{order_id}</code>\n\n"
            f"<b>Transfer ke Dana/QRIS Owner lalu kirim bukti ke</b> "
            f"<a href='tg://openmessage?user_id={OWNER_ID}'>Owner RANZ PEDIA</a></blockquote>",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="bahan")]]),
        )

    asyncio.create_task(auto_check_payment(user_id, order_id, role, durasi))



async def auto_check_payment(user_id: int, order_id: str, role: str, durasi: str):
    label_role = ROLE_LABEL.get(role, role.upper())
    label_durasi = DURASI_LABEL.get(durasi, durasi)
    max_wait = 60 * 30
    interval = 10
    elapsed = 0

    while elapsed < max_wait:
        await asyncio.sleep(interval)
        elapsed += interval

        if order_id not in pending_payments:
            return

        result = await pakasir_check_status(order_id)
        status = result.get("data", {}).get("status") or result.get("status")

        if status in ("paid", "success", "settlement", "capture"):
            pending_payments.pop(order_id, None)

            try:
                get_user = await bot.get_users(user_id)
                username = get_user.first_name
            except Exception:
                username = str(user_id)

            await proses_prem_user(user_id, role, durasi, bot)
            await kirim_notif_order(user_id, username, role, durasi, order_id)

            await bot.send_message(
                user_id,
                f"<blockquote><b>✅ Pembayaran Diterima!</b>\n\n"
                f"<b>🎫 Role:</b> {label_role}\n"
                f"<b>📆 Durasi:</b> {label_durasi}\n\n"
                f"<b>Sekarang kamu bisa langsung bikin userbot!</b></blockquote>",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🤖 Buat Userbot", callback_data="buat_ubot")
                ]]),
            )
            return

        elif status in ("failed", "expired", "cancelled", "cancel"):
            pending_payments.pop(order_id, None)
            await bot.send_message(
                user_id,
                "<blockquote><b>❌ Pembayaran Gagal / Expired</b>\n\n"
                "Coba order ulang ya! Kalo ada masalah hubungi owner.</blockquote>",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Order Lagi", callback_data="bahan")]]),
            )
            return

    pending_payments.pop(order_id, None)
    await bot.send_message(
        user_id,
        "<blockquote><b>⏰ Waktu pembayaran habis!</b>\n\n"
        "Kamu terlalu lama, order dibatalin otomatis.\n"
        "Coba lagi dari awal ya!</blockquote>",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Order Lagi", callback_data="bahan")]]),
    )


@PY.CALLBACK("^uprole_pick")
async def uprole_pick_callback(client, callback_query):
    data = callback_query.data.split()
    new_role = data[1]
    user_id = int(data[2])
    old_role = data[3]

    if callback_query.from_user.id != user_id:
        return await callback_query.answer("Ini bukan buat kamu!", show_alert=True)

    from PyroUbot.core.helpers.inline import BTN
    label_new = ROLE_LABEL.get(new_role, new_role.upper())

    text = (
        f"<blockquote><b>⬆️ Up Role ke: {label_new}</b>\n\n"
        f"<b>Pilih durasi baru kamu:</b></blockquote>"
    )
    return await callback_query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(BTN.DURASI_PICKER(new_role, user_id, is_uprole=True, old_role=old_role)),
    )


@PY.CALLBACK("^durasi_up")
async def durasi_up_callback(client, callback_query):
    data = callback_query.data.split()
    new_role = data[1]
    durasi = data[2]
    old_role = data[3]
    user_id = int(data[4])

    if callback_query.from_user.id != user_id:
        return await callback_query.answer("Bukan buat kamu!", show_alert=True)

    old_harga = ROLE_HARGA.get(old_role, {}).get(durasi, 0)
    new_harga = ROLE_HARGA.get(new_role, {}).get(durasi, 0)
    upgrade_harga = max(new_harga - old_harga, 0)

    label_old = ROLE_LABEL.get(old_role, old_role.upper())
    label_new = ROLE_LABEL.get(new_role, new_role.upper())
    label_durasi = DURASI_LABEL.get(durasi, durasi)

    from PyroUbot.core.helpers.inline import BTN
    order_id = f"RANZPEDIA-UP-{user_id}-{uuid.uuid4().hex[:8].upper()}"

    pending_payments[order_id] = {
        "user_id": user_id,
        "role": new_role,
        "durasi": durasi,
        "harga": upgrade_harga,
        "status": "pending",
        "is_upgrade": True,
    }

    text = (
        f"<blockquote><b>⬆️ Up Role Userbot</b>\n\n"
        f"<b>🎫 Role Sekarang:</b> {label_old}\n"
        f"<b>🚀 Role Baru:</b> {label_new}\n"
        f"<b>📆 Durasi:</b> {label_durasi}\n"
        f"<b>💰 Harga Upgrade:</b> Rp {upgrade_harga:,}\n"
        f"<b>🆔 Order ID:</b> <code>{order_id}</code>\n\n"
        f"<b>Klik Bayar Sekarang buat proses upgrade!</b></blockquote>"
    )
    return await callback_query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💳 Bayar Sekarang", callback_data=f"pakasir_pay {new_role} {durasi} {user_id}")],
            [InlineKeyboardButton("⬅️ Kembali", callback_data=f"bahan")],
        ]),
    )



@PY.CALLBACK("^(success|failed|home)")
async def admin_action_callback(client, callback_query):
    query = callback_query.data.split()
    action = query[0]

    if action == "home":
        user_id = callback_query.from_user.id
        from PyroUbot.core.helpers.inline import BTN
        from PyroUbot.core.helpers.text import MSG
        return await callback_query.edit_message_text(
            MSG.START(callback_query),
            reply_markup=InlineKeyboardMarkup(BTN.START(callback_query)),
        )

    user_target = int(query[1])
    try:
        get_user = await bot.get_users(user_target)
        full_name = get_user.first_name
    except Exception:
        full_name = str(user_target)

    if action == "success":
        role = query[2]
        durasi = query[3]
        label_role = ROLE_LABEL.get(role, role.upper())
        label_durasi = DURASI_LABEL.get(durasi, durasi)

        await proses_prem_user(user_target, role, durasi, bot)
        order_id = f"MANUAL-{user_target}"
        await kirim_notif_order(user_target, full_name, role, durasi, order_id)

        await bot.send_message(
            user_target,
            f"<blockquote><b>✅ Pembayaran Dikonfirmasi!</b>\n\n"
            f"<b>🎫 Role:</b> {label_role}\n"
            f"<b>📆 Durasi:</b> {label_durasi}\n\n"
            f"<b>Sekarang kamu bisa bikin userbot!</b></blockquote>",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🤖 Buat Userbot", callback_data="buat_ubot")]]),
        )
        return await callback_query.edit_message_caption(
            caption=f"<blockquote><b>✅ {full_name} berhasil dijadikan {label_role} ({label_durasi})</b></blockquote>",
        )

    if action == "failed":
        await bot.send_message(
            user_target,
            "<blockquote><b>❌ Pembayaran ditolak!</b>\n\n"
            "Bukti transfer tidak valid atau tidak sesuai.\n"
            "Coba bayar ulang dengan bukti yang benar ya!</blockquote>",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Coba Lagi", callback_data="bahan")]]),
        )
        return await callback_query.edit_message_caption(
            caption=f"<blockquote><b>❌ {full_name} ditolak.</b></blockquote>"
        )


@PY.CALLBACK("status")
async def cek_status_callback(client, callback_query):
    user_id = callback_query.from_user.id

    if user_id in ubot._get_my_id:
        exp = await get_expired_date(user_id)
        prefix = await get_pref(user_id)
        waktu = exp.strftime("%d-%m-%Y") if exp else "Tidak Ada"
        role = await get_user_current_role(user_id, bot.me.id)
        label_role = ROLE_LABEL.get(role, "Tidak Diketahui")

        return await callback_query.edit_message_text(
            f"<blockquote><b>📊 Status Userbot Kamu</b>\n\n"
            f"<b>✅ Status:</b> Aktif\n"
            f"<b>🎫 Role:</b> {label_role}\n"
            f"<b>⌨️ Prefix:</b> <code>{prefix[0] if prefix else '.'}</code>\n"
            f"<b>📅 Expired:</b> {waktu}</blockquote>",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data=f"home {user_id}")]]),
        )
    else:
        return await callback_query.edit_message_text(
            "<blockquote><b>❌ Kamu belum punya userbot aktif!</b>\n\n"
            "Beli dulu yuk!</blockquote>",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🛒 Beli Userbot", callback_data="bahan")],
                [InlineKeyboardButton("⬅️ Kembali", callback_data=f"home {user_id}")],
            ]),
        )


@PY.CALLBACK("up_role")
async def up_role_callback(client, callback_query):
    user_id = callback_query.from_user.id
    current_role = await get_user_current_role(user_id, bot.me.id)

    if current_role == "none":
        return await callback_query.edit_message_text(
            "<blockquote><b>❌ Kamu belum punya role apapun!</b>\n\nBeli dulu baru bisa upgrade.</blockquote>",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🛒 Beli Sekarang", callback_data="bahan")]]),
        )

    if current_role == "admin":
        return await callback_query.answer("Kamu udah role Admin, paling tinggi!", show_alert=True)

    label_current = ROLE_LABEL.get(current_role, current_role.upper())
    from PyroUbot.core.helpers.inline import BTN

    return await callback_query.edit_message_text(
        f"<blockquote><b>⬆️ Up Role Userbot</b>\n\n"
        f"<b>Role sekarang:</b> {label_current}\n\n"
        f"<b>Pilih role yang mau kamu upgrade ke:</b></blockquote>",
        reply_markup=InlineKeyboardMarkup(BTN.UP_ROLE_PICKER(user_id, current_role)),
    )
