from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from PyroUbot import OWNER_ID, bot, ubot, get_expired_date


class MSG:

    def EXP_MSG_UBOT(X):
        return (
            f"<blockquote><b>⚠️ PEMBERITAHUAN PENTING</b>\n\n"
            f"<b>Akun:</b> <a href='tg://user?id={X.me.id}'>{X.me.first_name} {X.me.last_name or ''}</a>\n"
            f"<b>ID:</b> <code>{X.me.id}</code>\n\n"
            f"<b>Masa aktif userbot kamu udah habis nih!</b>\n"
            f"Perpanjang sekarang biar bisa dipake lagi ya 🙏</blockquote>"
        )

    def START(message):
        return (
            f"<blockquote><b>👋 Halo, <a href='tg://user?id={message.from_user.id}'>"
            f"{message.from_user.first_name} {message.from_user.last_name or ''}</a>!</b>\n\n"
            f"<b>Selamat datang di <a href='t.me/{bot.me.username}'>RANZ PEDIA</a> 🎉</b>\n\n"
            f"<b>Bot ini bisa bantu kamu bikin userbot dengan gampang banget!</b>\n\n"
            f"<b>📌 Cara beli userbot:</b>\n"
            f"<b>1.</b> Klik tombol <b>Beli Userbot</b> di bawah\n"
            f"<b>2.</b> Pilih role yang kamu mau (Member / Seles / Admin)\n"
            f"<b>3.</b> Tentuin durasi (1 Bulan / Permanen)\n"
            f"<b>4.</b> Scan QRIS yang muncul & bayar\n"
            f"<b>5.</b> Bot otomatis konfirmasi begitu bayar masuk\n"
            f"<b>6.</b> Aktifkan userbot kamu & langsung gas!\n\n"
            f"<b>💬 Ada kendala? Hubungi <a href='tg://openmessage?user_id={OWNER_ID}'>Owner</a> langsung aja!</b></blockquote>"
        )

    def TEXT_PAYMENT(harga, total, bulan):
        return (
            f"<blockquote><b>💳 INFO PEMBAYARAN</b>\n\n"
            f"<b>Harga per bulan:</b> Rp {harga}.000\n"
            f"<b>Metode bayar:</b> QRIS All Payment\n"
            f"<b>Total harga:</b> Rp {total}.000\n"
            f"<b>Durasi:</b> {bulan} Bulan\n\n"
            f"<b>Owner:</b> <a href='tg://openmessage?user_id={OWNER_ID}'>RANZ PEDIA</a>\n\n"
            f"<b>Klik tombol konfirmasi buat lanjut pembayaran ya!</b></blockquote>"
        )

    async def UBOT(count):
        return (
            f"<blockquote><b>📋 RANZ PEDIA — Userbot ke-{int(count) + 1}/{len(ubot._ubot)}</b>\n\n"
            f"<b>Akun:</b> <a href='tg://user?id={ubot._ubot[int(count)].me.id}'>"
            f"{ubot._ubot[int(count)].me.first_name} {ubot._ubot[int(count)].me.last_name or ''}</a>\n"
            f"<b>User ID:</b> <code>{ubot._ubot[int(count)].me.id}</code></blockquote>"
        )

    def POLICY():
        return (
            f"<blockquote><b>⚠️ Kamu belum beli userbot nih!</b>\n\n"
            f"Hubungi <a href='tg://openmessage?user_id={OWNER_ID}'>Owner RANZ PEDIA</a> buat info lebih lanjut.</blockquote>"
        )

    def DEAK(X):
        return (
            f"<blockquote><b>🗑️ Akun berhasil dideaktivasi</b>\n\n"
            f"<b>Akun:</b> {X.me.first_name} {X.me.last_name or ''}\n"
            f"<b>ID:</b> <code>{X.me.id}</code></blockquote>"
        )
