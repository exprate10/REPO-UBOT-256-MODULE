import asyncio
import random
import string
import time
import io
from datetime import datetime

import aiohttp
import qrcode
from dateutil.relativedelta import relativedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytz import timezone

from PyroUbot import *
from PyroUbot.config import PAKASIR_API_KEY, PAKASIR_PROJECT, LOGS_MAKER_UBOT, OWNER_ID

__MODULE__ = "ᴘᴀʏᴍᴇɴᴛ"
__HELP__ = """
<blockquote><b>PAYMENT — RANZ PEDIA</b>

Sistem pembayaran otomatis via QRIS Pakasir.
Bot langsung konfirmasi begitu saldo masuk.</blockquote>
"""

PAKASIR_BASE = "https://app.pakasir.com/api"

ROLE_HARGA = {
    "member": {"1": 2000,  "0": 3000},
    "seles":  {"1": 4000,  "0": 5000},
    "admin":  {"1": 10000, "0": 15000},
}

ROLE_LABEL = {
    "member": "Member",
    "seles":  "Seles",
    "admin":  "Admin",
}

DURASI_LABEL = {
    "1": "1 Bulan",
    "0": "Permanen",
}

pending_payments = {}


def generate_order_id() -> str:
    rand = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"TRX-{int(time.time() * 1000)}-{rand}"


def buat_foto_qris(qr_string: str) -> io.BytesIO:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_string)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    buf.name = "qris.png"
    return buf


async def pakasir_create_qris(amount: int, order_id: str) -> dict:
    url = f"{PAKASIR_BASE}/transactioncreate/qris"
    payload = {
        "project":  PAKASIR_PROJECT,
        "order_id": order_id,
        "amount":   amount,
        "api_key":  PAKASIR_API_KEY,
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=aiohttp.ClientTimeout(total=15),
            ) as resp:
                return await resp.json()
    except Exception as e:
        return {"error": str(e)}


async def pakasir_check_status(order_id: str, amount: int) -> bool:
    url = (
        f"{PAKASIR_BASE}/transactiondetail"
        f"?project={PAKASIR_PROJECT}"
        f"&amount={amount}"
        f"&order_id={order_id}"
        f"&api_key={PAKASIR_API_KEY}"
    )
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                timeout=aiohttp.ClientTimeout(total=10),
            ) as resp:
                if resp.status == 404:
                    return False
                data = await resp.json()
                trx = data.get("transaction", {})
                return trx.get("status") == "completed"
    except Exception:
        return False


async def get_role_user(user_id: int, bot_id: int) -> str:
    admin_list = await get_list_from_vars(bot_id, "ADMIN_USERS")
    seles_list = await get_list_from_vars(bot_id, "SELER_USERS")
    prem_list  = await get_list_from_vars(bot_id, "PREM_USERS")
    if user_id in admin_list:
        return "admin"
    if user_id in seles_list:
        return "seles"
    if user_id in prem_list:
        return "member"
    return "none"


async def aktifkan_user(user_id: int, role: str, durasi: str):
    bot_id = bot.me.id

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
    exp = now + relativedelta(months=1) if durasi == "1" else now + relativedelta(years=100)
    await set_expired_date(user_id, exp)


async def notif_order_sukses(user_id: int, nama: str, role: str, durasi: str, order_id: str):
    waktu        = datetime.now(timezone("Asia/Jakarta")).strftime("%d-%m-%Y %H:%M:%S")
    label_role   = ROLE_LABEL.get(role, role)
    label_durasi = DURASI_LABEL.get(durasi, durasi)
    harga        = ROLE_HARGA.get(role, {}).get(durasi, 0)

    teks = (
        f"<blockquote>"
        f"<b>&#x2713; ORDER SUKSES — RANZ PEDIA</b>\n\n"
        f"<b>User    :</b> <a href='tg://user?id={user_id}'>{nama}</a>\n"
        f"<b>User ID :</b> <code>{user_id}</code>\n"
        f"<b>Order ID:</b> <code>{order_id}</code>\n"
        f"<b>Role    :</b> {label_role}\n"
        f"<b>Durasi  :</b> {label_durasi}\n"
        f"<b>Nominal :</b> Rp {harga:,}\n"
        f"<b>Waktu   :</b> {waktu}"
        f"</blockquote>"
    )
    try:
        await bot.send_message(LOGS_MAKER_UBOT, teks)
    except Exception as e:
        print(f"[PAYMENT] Gagal kirim notif log: {e}")


async def loop_cek_bayar(user_id: int, order_id: str, amount: int, role: str, durasi: str):
    label_role   = ROLE_LABEL.get(role, role)
    label_durasi = DURASI_LABEL.get(durasi, durasi)
    max_detik    = 30 * 60
    interval     = 10
    elapsed      = 0

    while elapsed < max_detik:
        await asyncio.sleep(interval)
        elapsed += interval

        if order_id not in pending_payments:
            return

        lunas = await pakasir_check_status(order_id, amount)

        if lunas:
            pending_payments.pop(order_id, None)

            try:
                user_obj = await bot.get_users(user_id)
                nama     = user_obj.first_name
            except Exception:
                nama = str(user_id)

            await aktifkan_user(user_id, role, durasi)
            await notif_order_sukses(user_id, nama, role, durasi, order_id)

            await bot.send_message(
                user_id,
                (
                    f"<blockquote>"
                    f"<b>&#x2713; Pembayaran Diterima!</b>\n\n"
                    f"<b>Role   :</b> {label_role}\n"
                    f"<b>Durasi :</b> {label_durasi}\n\n"
                    f"Sekarang langsung bikin userbot kamu ya!"
                    f"</blockquote>"
                ),
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("Buat Userbot", callback_data="buat_ubot"),
                ]]),
            )
            return

    pending_payments.pop(order_id, None)
    await bot.send_message(
        user_id,
        (
            "<blockquote>"
            "<b>&#x23; Waktu Bayar Habis</b>\n\n"
            "Udah 30 menit tapi bayaran belum masuk, "
            "order dibatalin otomatis.\n"
            "Coba order lagi dari awal ya."
            "</blockquote>"
        ),
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Order Lagi", callback_data="bahan"),
        ]]),
    )


@PY.CALLBACK("bahan")
async def cb_pilih_role(client, callback_query):
    uid = callback_query.from_user.id

    if uid in ubot._get_my_id:
        return await callback_query.edit_message_text(
            (
                "<blockquote>"
                "<b>Kamu udah punya userbot aktif.</b>\n\n"
                "Kalau ubotnya ga respon, coba restart dulu."
                "</blockquote>"
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Restart Userbot", callback_data="ress_ubot")],
                [InlineKeyboardButton("Kembali", callback_data=f"home {uid}")],
            ]),
        )

    if len(ubot._ubot) + 1 > MAX_BOT:
        return await callback_query.edit_message_text(
            (
                f"<blockquote>"
                f"<b>Slot userbot lagi penuh.</b>\n\n"
                f"Total sekarang: {len(ubot._ubot)} slot.\n"
                f"Hubungi <a href='tg://openmessage?user_id={OWNER_ID}'>Owner</a> dulu ya."
                f"</blockquote>"
            ),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Kembali", callback_data=f"home {uid}"),
            ]]),
        )

    return await callback_query.edit_message_text(
        (
            "<blockquote>"
            "<b>Pilih Role Userbot</b>\n\n"
            "<b>Member</b>  — fitur standar\n"
            "<b>Seles</b>   — fitur standar + bisa jual ubot\n"
            "<b>Admin</b>   — akses penuh semua fitur\n\n"
            "Pilih yang kamu mau:"
            "</blockquote>"
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Member", callback_data=f"role_pick member {uid}")],
            [InlineKeyboardButton("Seles",  callback_data=f"role_pick seles {uid}")],
            [InlineKeyboardButton("Admin",  callback_data=f"role_pick admin {uid}")],
            [InlineKeyboardButton("Kembali", callback_data=f"home {uid}")],
        ]),
    )


@PY.CALLBACK("^role_pick")
async def cb_role_pick(client, callback_query):
    parts  = callback_query.data.split()
    role   = parts[1]
    uid    = int(parts[2])

    if callback_query.from_user.id != uid:
        return await callback_query.answer("Ini bukan buat kamu.", show_alert=True)

    label  = ROLE_LABEL.get(role, role)
    harga1 = ROLE_HARGA[role]["1"]
    harga0 = ROLE_HARGA[role]["0"]

    return await callback_query.edit_message_text(
        (
            f"<blockquote>"
            f"<b>Role dipilih: {label}</b>\n\n"
            f"Sekarang pilih durasi:\n"
            f"<b>1 Bulan</b>   — Rp {harga1:,}\n"
            f"<b>Permanen</b>  — Rp {harga0:,}"
            f"</blockquote>"
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("1 Bulan",  callback_data=f"durasi_pick {role} 1 {uid}")],
            [InlineKeyboardButton("Permanen", callback_data=f"durasi_pick {role} 0 {uid}")],
            [InlineKeyboardButton("Kembali",  callback_data="bahan")],
        ]),
    )


@PY.CALLBACK("^durasi_pick")
async def cb_durasi_pick(client, callback_query):
    parts  = callback_query.data.split()
    role   = parts[1]
    durasi = parts[2]
    uid    = int(parts[3])

    if callback_query.from_user.id != uid:
        return await callback_query.answer("Ini bukan buat kamu.", show_alert=True)

    label_role   = ROLE_LABEL.get(role, role)
    label_durasi = DURASI_LABEL.get(durasi, durasi)
    harga        = ROLE_HARGA.get(role, {}).get(durasi, 0)

    return await callback_query.edit_message_text(
        (
            f"<blockquote>"
            f"<b>Ringkasan Order</b>\n\n"
            f"<b>Role  :</b> {label_role}\n"
            f"<b>Durasi:</b> {label_durasi}\n"
            f"<b>Harga :</b> Rp {harga:,}\n\n"
            f"Klik <b>Bayar Sekarang</b> buat lanjut ke QRIS."
            f"</blockquote>"
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Bayar Sekarang", callback_data=f"pakasir_pay {role} {durasi} {uid}")],
            [InlineKeyboardButton("Kembali",        callback_data=f"role_pick {role} {uid}")],
        ]),
    )


@PY.CALLBACK("^pakasir_pay")
async def cb_pakasir_pay(client, callback_query):
    parts  = callback_query.data.split()
    role   = parts[1]
    durasi = parts[2]
    uid    = int(parts[3])

    if callback_query.from_user.id != uid:
        return await callback_query.answer("Ini bukan buat kamu.", show_alert=True)

    label_role   = ROLE_LABEL.get(role, role)
    label_durasi = DURASI_LABEL.get(durasi, durasi)
    harga        = ROLE_HARGA.get(role, {}).get(durasi, 0)
    order_id     = generate_order_id()

    await callback_query.edit_message_text(
        "<blockquote><b>Lagi bikin QRIS kamu, tunggu sebentar...</b></blockquote>"
    )

    hasil = await pakasir_create_qris(harga, order_id)

    payment  = hasil.get("payment") if hasil and not hasil.get("error") else None
    qr_str   = payment.get("payment_number") if payment else None

    if not qr_str:
        pending_payments.pop(order_id, None)
        return await callback_query.edit_message_text(
            (
                f"<blockquote>"
                f"<b>Gagal bikin QRIS.</b>\n\n"
                f"<b>Role  :</b> {label_role}\n"
                f"<b>Durasi:</b> {label_durasi}\n"
                f"<b>Harga :</b> Rp {harga:,}\n\n"
                f"Transfer manual ke QRIS Owner lalu kirim bukti ke "
                f"<a href='tg://openmessage?user_id={OWNER_ID}'>Owner RANZ PEDIA</a>.\n"
                f"<b>Order ID:</b> <code>{order_id}</code>"
                f"</blockquote>"
            ),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Kembali", callback_data="bahan"),
            ]]),
        )

    pending_payments[order_id] = {
        "user_id": uid,
        "role":    role,
        "durasi":  durasi,
        "harga":   harga,
    }

    caption = (
        f"<blockquote>"
        f"<b>QRIS Pembayaran — RANZ PEDIA</b>\n\n"
        f"<b>Role    :</b> {label_role}\n"
        f"<b>Durasi  :</b> {label_durasi}\n"
        f"<b>Total   :</b> Rp {harga:,}\n"
        f"<b>Order ID:</b> <code>{order_id}</code>\n\n"
        f"Scan QRIS di atas pakai aplikasi e-wallet atau bank kamu.\n"
        f"Bot otomatis konfirmasi begitu saldo masuk."
        f"</blockquote>"
    )

    foto_qris = buat_foto_qris(qr_str)

    try:
        await callback_query.message.delete()
    except Exception:
        pass

    await bot.send_photo(
        uid,
        photo=foto_qris,
        caption=caption,
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Batalkan Order", callback_data=f"batal_order {order_id} {uid}"),
        ]]),
    )

    asyncio.create_task(loop_cek_bayar(uid, order_id, harga, role, durasi))


@PY.CALLBACK("^batal_order")
async def cb_batal_order(client, callback_query):
    parts    = callback_query.data.split()
    order_id = parts[1]
    uid      = int(parts[2])

    if callback_query.from_user.id != uid:
        return await callback_query.answer("Ini bukan buat kamu.", show_alert=True)

    pending_payments.pop(order_id, None)

    await callback_query.message.delete()
    await bot.send_message(
        uid,
        "<blockquote><b>Order dibatalin.</b>\n\nKalau mau order lagi klik tombol di bawah.</blockquote>",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Order Lagi", callback_data="bahan"),
        ]]),
    )


@PY.CALLBACK("^uprole_pick")
async def cb_uprole_pick(client, callback_query):
    parts    = callback_query.data.split()
    new_role = parts[1]
    uid      = int(parts[2])
    old_role = parts[3]

    if callback_query.from_user.id != uid:
        return await callback_query.answer("Ini bukan buat kamu.", show_alert=True)

    label_new = ROLE_LABEL.get(new_role, new_role)

    return await callback_query.edit_message_text(
        (
            f"<blockquote>"
            f"<b>Up Role ke: {label_new}</b>\n\n"
            f"Pilih durasi baru:"
            f"</blockquote>"
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("1 Bulan",  callback_data=f"durasi_up {new_role} 1 {old_role} {uid}")],
            [InlineKeyboardButton("Permanen", callback_data=f"durasi_up {new_role} 0 {old_role} {uid}")],
            [InlineKeyboardButton("Kembali",  callback_data="bahan")],
        ]),
    )


@PY.CALLBACK("^durasi_up")
async def cb_durasi_up(client, callback_query):
    parts    = callback_query.data.split()
    new_role = parts[1]
    durasi   = parts[2]
    old_role = parts[3]
    uid      = int(parts[4])

    if callback_query.from_user.id != uid:
        return await callback_query.answer("Ini bukan buat kamu.", show_alert=True)

    old_harga    = ROLE_HARGA.get(old_role, {}).get(durasi, 0)
    new_harga    = ROLE_HARGA.get(new_role, {}).get(durasi, 0)
    harga_up     = max(new_harga - old_harga, 0)
    label_old    = ROLE_LABEL.get(old_role, old_role)
    label_new    = ROLE_LABEL.get(new_role, new_role)
    label_durasi = DURASI_LABEL.get(durasi, durasi)
    order_id     = generate_order_id()

    pending_payments[order_id] = {
        "user_id":    uid,
        "role":       new_role,
        "durasi":     durasi,
        "harga":      harga_up,
        "is_upgrade": True,
    }

    return await callback_query.edit_message_text(
        (
            f"<blockquote>"
            f"<b>Up Role Userbot</b>\n\n"
            f"<b>Role Sekarang :</b> {label_old}\n"
            f"<b>Role Baru     :</b> {label_new}\n"
            f"<b>Durasi        :</b> {label_durasi}\n"
            f"<b>Harga Upgrade :</b> Rp {harga_up:,}\n"
            f"<b>Order ID      :</b> <code>{order_id}</code>\n\n"
            f"Klik <b>Bayar Sekarang</b> buat lanjut ke QRIS."
            f"</blockquote>"
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Bayar Sekarang", callback_data=f"pakasir_pay {new_role} {durasi} {uid}")],
            [InlineKeyboardButton("Kembali",        callback_data="bahan")],
        ]),
    )


@PY.CALLBACK("up_role")
async def cb_up_role(client, callback_query):
    uid          = callback_query.from_user.id
    current_role = await get_role_user(uid, bot.me.id)

    if current_role == "none":
        return await callback_query.edit_message_text(
            (
                "<blockquote>"
                "<b>Kamu belum punya role apapun.</b>\n\n"
                "Beli dulu baru bisa upgrade."
                "</blockquote>"
            ),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Beli Sekarang", callback_data="bahan"),
            ]]),
        )

    if current_role == "admin":
        return await callback_query.answer("Kamu udah role Admin, itu yang paling tinggi.", show_alert=True)

    label_current = ROLE_LABEL.get(current_role, current_role)
    role_order    = ["member", "seles", "admin"]
    role_idx      = role_order.index(current_role)
    tombol        = []

    for i, r in enumerate(role_order):
        if i > role_idx:
            tombol.append([InlineKeyboardButton(
                f"Up ke {ROLE_LABEL.get(r, r)}",
                callback_data=f"uprole_pick {r} {uid} {current_role}",
            )])

    tombol.append([InlineKeyboardButton("Kembali", callback_data=f"home {uid}")])

    return await callback_query.edit_message_text(
        (
            f"<blockquote>"
            f"<b>Up Role Userbot</b>\n\n"
            f"<b>Role sekarang:</b> {label_current}\n\n"
            f"Mau upgrade ke role mana?"
            f"</blockquote>"
        ),
        reply_markup=InlineKeyboardMarkup(tombol),
    )


@PY.CALLBACK("status")
async def cb_status(client, callback_query):
    uid = callback_query.from_user.id

    if uid not in ubot._get_my_id:
        return await callback_query.edit_message_text(
            (
                "<blockquote>"
                "<b>Kamu belum punya userbot aktif.</b>\n\n"
                "Beli dulu baru bisa cek status."
                "</blockquote>"
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Beli Userbot", callback_data="bahan")],
                [InlineKeyboardButton("Kembali",      callback_data=f"home {uid}")],
            ]),
        )

    exp          = await get_expired_date(uid)
    prefix       = await get_pref(uid)
    waktu_exp    = exp.strftime("%d-%m-%Y") if exp else "Tidak ada"
    role         = await get_role_user(uid, bot.me.id)
    label_role   = ROLE_LABEL.get(role, "Tidak diketahui")

    return await callback_query.edit_message_text(
        (
            f"<blockquote>"
            f"<b>Status Userbot Kamu</b>\n\n"
            f"<b>Status  :</b> Aktif\n"
            f"<b>Role    :</b> {label_role}\n"
            f"<b>Prefix  :</b> <code>{prefix[0] if prefix else '.'}</code>\n"
            f"<b>Expired :</b> {waktu_exp}"
            f"</blockquote>"
        ),
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Kembali", callback_data=f"home {uid}"),
        ]]),
    )


@PY.CALLBACK("^(success|failed)")
async def cb_admin_aksi(client, callback_query):
    parts  = callback_query.data.split()
    action = parts[0]

    if callback_query.from_user.id != OWNER_ID:
        return await callback_query.answer("Ini khusus owner.", show_alert=True)

    uid_target = int(parts[1])

    try:
        user_obj = await bot.get_users(uid_target)
        nama     = user_obj.first_name
    except Exception:
        nama = str(uid_target)

    if action == "success":
        role         = parts[2]
        durasi       = parts[3]
        label_role   = ROLE_LABEL.get(role, role)
        label_durasi = DURASI_LABEL.get(durasi, durasi)

        await aktifkan_user(uid_target, role, durasi)
        await notif_order_sukses(uid_target, nama, role, durasi, f"MANUAL-{uid_target}")

        await bot.send_message(
            uid_target,
            (
                f"<blockquote>"
                f"<b>Pembayaran dikonfirmasi!</b>\n\n"
                f"<b>Role  :</b> {label_role}\n"
                f"<b>Durasi:</b> {label_durasi}\n\n"
                f"Sekarang langsung bikin userbot kamu ya."
                f"</blockquote>"
            ),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Buat Userbot", callback_data="buat_ubot"),
            ]]),
        )
        return await callback_query.edit_message_caption(
            caption=(
                f"<blockquote>"
                f"<b>{nama} berhasil diaktifkan sebagai {label_role} ({label_durasi}).</b>"
                f"</blockquote>"
            ),
        )

    await bot.send_message(
        uid_target,
        (
            "<blockquote>"
            "<b>Pembayaran ditolak.</b>\n\n"
            "Bukti transfer tidak valid atau tidak sesuai.\n"
            "Kalau ada masalah hubungi owner langsung."
            "</blockquote>"
        ),
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Coba Lagi", callback_data="bahan"),
        ]]),
    )
    return await callback_query.edit_message_caption(
        caption=f"<blockquote><b>{nama} ditolak.</b></blockquote>"
    )


@PY.CALLBACK("^home")
async def cb_home(client, callback_query):
    from PyroUbot.core.helpers.inline import BTN
    from PyroUbot.core.helpers.text import MSG
    uid = callback_query.from_user.id
    try:
        await callback_query.message.delete()
        await bot.send_photo(
            uid,
            photo="https://i.imgur.com/7BTzIeo.png",
            caption=MSG.START(callback_query),
            reply_markup=InlineKeyboardMarkup(BTN.START(callback_query)),
        )
    except Exception:
        await callback_query.edit_message_text(
            MSG.START(callback_query),
            reply_markup=InlineKeyboardMarkup(BTN.START(callback_query)),
        )
