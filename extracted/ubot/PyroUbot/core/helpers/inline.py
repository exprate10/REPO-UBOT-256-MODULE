import re
from pykeyboard import InlineKeyboard
from pyrogram.errors import MessageNotModified
from pyrogram.types import *
from pyromod.helpers import ikb
from pyrogram.types import (
    InlineKeyboardButton,
    InlineQueryResultArticle,
    InputTextMessageContent,
)

from PyroUbot import *


def detect_url_links(text):
    link_pattern = (
        r"(?:https?://)?(?:www\.)?[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})+(?:[/?]\S+)?"
    )
    link_found = re.findall(link_pattern, text)
    return link_found


def detect_button_and_text(text):
    button_matches = re.findall(r"\| ([^|]+) - ([^|]+) \|", text)
    text_matches = (
        re.search(r"(.*?) \|", text, re.DOTALL).group(1) if "|" in text else text
    )
    return button_matches, text_matches


def create_inline_keyboard(text, user_id=False, is_back=False):
    keyboard = []
    button_matches, text_matches = detect_button_and_text(text)

    prev_button_data = None
    for button_text, button_data in button_matches:
        data = (
            button_data.split("#")[0]
            if detect_url_links(button_data.split("#")[0])
            else f"_gtnote {int(user_id.split('_')[0])}_{user_id.split('_')[1]} {button_data.split('#')[0]}"
        )
        cb_data = data if user_id else button_data.split("#")[0]
        if "#" in button_data:
            if prev_button_data:
                if detect_url_links(cb_data):
                    keyboard[-1].append(InlineKeyboardButton(button_text, url=cb_data))
                else:
                    keyboard[-1].append(
                        InlineKeyboardButton(button_text, callback_data=cb_data)
                    )
            else:
                if detect_url_links(cb_data):
                    button_row = [InlineKeyboardButton(button_text, url=cb_data)]
                else:
                    button_row = [
                        InlineKeyboardButton(button_text, callback_data=cb_data)
                    ]
                keyboard.append(button_row)
        else:
            if button_data.startswith("http"):
                button_row = [InlineKeyboardButton(button_text, url=cb_data)]
            else:
                button_row = [InlineKeyboardButton(button_text, callback_data=cb_data)]
            keyboard.append(button_row)

        prev_button_data = button_data

    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    if user_id and is_back:
        markup.inline_keyboard.append(
            [
                InlineKeyboardButton(
                    "⬅️ Kembali",
                    f"_gtnote {int(user_id.split('_')[0])}_{user_id.split('_')[1]}",
                )
            ]
        )

    return markup, text_matches


class BTN:

    def ALIVE(get_id):
        return [
            [
                InlineKeyboardButton(
                    text="✖️ Tutup",
                    callback_data=f"alv_cls {int(get_id[1])} {int(get_id[2])}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📋 Help",
                    callback_data="help_back",
                )
            ],
        ]

    def PROMODEK(message):
        return [
            [InlineKeyboardButton("✅ Setuju & Lanjutkan", callback_data="bahan")],
        ]

    def BOT_HELP(message):
        return [
            [InlineKeyboardButton("🔄 Restart", callback_data="reboot")],
            [InlineKeyboardButton("📊 System", callback_data="system")],
            [InlineKeyboardButton("🤖 Ubot", callback_data="ubot")],
            [InlineKeyboardButton("⬆️ Update", callback_data="update")],
        ]

    def START(message):
        user_id = message.from_user.id
        if user_id != OWNER_ID:
            return [
                [InlineKeyboardButton("🛒 Beli Userbot", callback_data="bahan")],
                [InlineKeyboardButton("◉ Channel Resmi", url="https://t.me/ranzpedia_bot")],
                [
                    InlineKeyboardButton("🤖 Buat Userbot", callback_data="buat_ubot"),
                    InlineKeyboardButton("📋 Help Menu", callback_data="help_back"),
                ],
                [InlineKeyboardButton("💬 Support", callback_data="support")],
                [InlineKeyboardButton("📊 Cek Status", callback_data=f"status")],
            ]
        else:
            return [
                [InlineKeyboardButton("🤖 Buat Userbot", callback_data="bahan")],
                [
                    InlineKeyboardButton("⬆️ Git Pull", callback_data="cb_gitpull"),
                    InlineKeyboardButton("🔄 Restart", callback_data="cb_restart"),
                ],
                [InlineKeyboardButton("📋 List Userbot", callback_data="cek_ubot")],
            ]

    def ROLE_PICKER(user_id):
        return [
            [InlineKeyboardButton("👤 Member", callback_data=f"role_pick member {user_id}")],
            [InlineKeyboardButton("💼 Seles", callback_data=f"role_pick seles {user_id}")],
            [InlineKeyboardButton("⚙️ Admin", callback_data=f"role_pick admin {user_id}")],
            [InlineKeyboardButton("⬅️ Kembali", callback_data=f"home {user_id}")],
        ]

    def UP_ROLE_PICKER(user_id, current_role):
        btns = []
        role_order = ["member", "seles", "admin"]
        role_idx = role_order.index(current_role) if current_role in role_order else -1
        for i, r in enumerate(role_order):
            if i > role_idx:
                btns.append([InlineKeyboardButton(
                    f"⬆️ Up ke {r.capitalize()}",
                    callback_data=f"uprole_pick {r} {user_id} {current_role}"
                )])
        btns.append([InlineKeyboardButton("⬅️ Kembali", callback_data=f"home {user_id}")])
        return btns

    def DURASI_PICKER(role, user_id, is_uprole=False, old_role=""):
        prefix = "durasi_up" if is_uprole else "durasi_pick"
        extra = f" {old_role}" if is_uprole else ""
        return [
            [InlineKeyboardButton("📅 1 Bulan", callback_data=f"{prefix} {role} 1{extra} {user_id}")],
            [InlineKeyboardButton("♾️ Permanen", callback_data=f"{prefix} {role} 0{extra} {user_id}")],
            [InlineKeyboardButton("⬅️ Kembali", callback_data=f"bahan")],
        ]

    def KONFIRMASI_BAYAR(role, durasi, user_id):
        return [
            [InlineKeyboardButton("💳 Bayar Sekarang", callback_data=f"pakasir_pay {role} {durasi} {user_id}")],
            [InlineKeyboardButton("⬅️ Kembali", callback_data=f"bahan")],
        ]

    def ADD_EXP(user_id):
        buttons = InlineKeyboard(row_width=3)
        keyboard = []
        for X in range(1, 13):
            keyboard.append(
                InlineKeyboardButton(
                    f"{X} Bulan",
                    callback_data=f"success {user_id} member {X}",
                )
            )
        buttons.add(*keyboard)
        buttons.row(
            InlineKeyboardButton("👤 Lihat Profil", callback_data=f"profil {user_id}")
        )
        buttons.row(
            InlineKeyboardButton("❌ Tolak Pembayaran", callback_data=f"failed {user_id}")
        )
        return buttons

    def EXP_UBOT():
        return [
            [InlineKeyboardButton("🛒 Beli Userbot", callback_data="bahan")],
        ]

    def UBOT(user_id, count):
        return [
            [
                InlineKeyboardButton(
                    "🗑️ Hapus dari Database",
                    callback_data=f"del_ubot {int(user_id)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "⏳ Cek Masa Aktif",
                    callback_data=f"cek_masa_aktif {int(user_id)}",
                )
            ],
            [
                InlineKeyboardButton("⬅️ Sebelumnya", callback_data=f"p_ub {int(count)}"),
                InlineKeyboardButton("Selanjutnya ➡️", callback_data=f"n_ub {int(count)}"),
            ],
        ]

    def DEAK(user_id, count):
        return [
            [
                InlineKeyboardButton("⬅️ Kembali", callback_data=f"p_ub {int(count)}"),
                InlineKeyboardButton("✅ Setujui", callback_data=f"deak_akun {int(count)}"),
            ],
        ]
