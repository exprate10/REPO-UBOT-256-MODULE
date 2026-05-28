import random
import re
import os
import platform
import subprocess
import sys
from datetime import datetime
from io import BytesIO, StringIO
from PyroUbot.config import OWNER_ID
import psutil
from PyroUbot import *
from time import time
from pyrogram.types import (
    InlineQueryResultPhoto,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from pyrogram import Client
from pyrogram.raw.functions import Ping
from pyrogram.types import *


@PY.BOT("joinreseller")
async def joinreseller_handler(client, message):
    from PyroUbot.core.helpers.inline import BTN
    buttons = BTN.PROMODEK(message)
    await message.reply(
        "<blockquote><b>◈ Join Reseller — Rp 15.000</b>\n\n"
        "<b>⌯ Rules Reseller:</b>\n"
        "<b>•</b> Bertanggung jawab penuh atas transaksi\n"
        "<b>•</b> Dilarang scam / penipuan\n"
        "<b>•</b> Wajib punya Bank / E-Wallet aktif\n"
        "<b>•</b> Dilarang bagi akses userbot gratis\n\n"
        "<b>📚 Keuntungan Reseller:</b>\n"
        "<b>•</b> Dasar jualan yang kuat\n"
        "<b>•</b> Akses reseller selamanya setelah beli\n"
        "<b>•</b> Bebas add/create userbot tanpa batas\n"
        "<b>•</b> No refund setelah bayar\n\n"
        "<b>Setuju & mau daftar? Klik tombol di bawah!</b></blockquote>",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@PY.UBOT("alive")
@PY.TOP_CMD
async def alive_handler(client, message):
    try:
        x = await client.get_inline_bot_results(
            bot.me.username, f"alive {message.id} {client.me.id}"
        )
        await message.reply_inline_bot_result(x.query_id, x.results[0].id, quote=True)
    except Exception as error:
        await message.reply(f"<blockquote><b>⌭ Error:</b> {error}</blockquote>")


@PY.INLINE("^alive")
async def alive_inline(client, inline_query):
    psr = await EMO.PASIR(client)
    get_id = inline_query.query.split()
    for my in ubot._ubot:
        if int(get_id[2]) == my.me.id:
            try:
                peer = my._get_my_peer[my.me.id]
                users = len(peer["pm"])
                group = len(peer["gc"])
            except Exception:
                users = random.randrange(await my.get_dialogs_count())
                group = random.randrange(await my.get_dialogs_count())

            get_exp = await get_expired_date(my.me.id)
            exp = get_exp.strftime("%d-%m-%Y") if get_exp else "ga ada"

            ultra_list = await get_list_from_vars(client.me.id, "ULTRA_PREM")
            status = "SuperUltra" if my.me.id in ultra_list else "Premium"

            button = BTN.ALIVE(get_id)
            start = datetime.now()
            await my.invoke(Ping(ping_id=0))
            ping = (datetime.now() - start).microseconds / 1000
            uptime = await get_time((time() - start_time))

            msg = (
                f"<blockquote><b>{bot.me.mention}</b>\n\n"
                f"<b>Status:</b> {status}\n"
                f"<b>{psr} Expired:</b> {exp}\n"
                f"<b>DC ID:</b> {my.me.dc_id}\n"
                f"<b>Ping DC:</b> {ping} ms\n"
                f"<b>Users:</b> {users} users\n"
                f"<b>Groups:</b> {group} group\n"
                f"<b>Uptime:</b> {uptime}\n\n"
                f"<b>RANZ PEDIA — Userbot Premium</b></blockquote>"
            )
            await client.answer_inline_query(
                inline_query.id,
                cache_time=300,
                results=[
                    InlineQueryResultArticle(
                        title="◱",
                        reply_markup=InlineKeyboardMarkup(button),
                        input_message_content=InputTextMessageContent(msg),
                    )
                ],
            )


@PY.CALLBACK("alv_cls")
async def alv_cls_callback(client, callback_query):
    get_id = callback_query.data.split()
    if callback_query.from_user.id != int(get_id[2]):
        return
    unPacked = unpackInlineMessage(callback_query.inline_message_id)
    for my in ubot._ubot:
        if callback_query.from_user.id == int(my.me.id):
            await my.delete_messages(
                unPacked.chat_id, [int(get_id[1]), unPacked.message_id]
            )


@PY.BOT("anu")
@PY.ADMIN
async def anu_handler(client, message):
    from PyroUbot.core.helpers.inline import BTN
    buttons = BTN.BOT_HELP(message)
    await message.reply(
        "<blockquote><b>⌘ Panel Kontrol Bot RANZ PEDIA</b></blockquote>",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@PY.CALLBACK("balik")
async def balik_callback(client, callback_query):
    from PyroUbot.core.helpers.inline import BTN
    buttons = BTN.BOT_HELP(callback_query)
    await callback_query.edit_message_text(
        "<blockquote><b>⌘ Panel Kontrol Bot RANZ PEDIA</b></blockquote>",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@PY.CALLBACK("reboot")
async def reboot_callback(client, callback_query):
    user_id = callback_query.from_user.id
    admin_list = await get_list_from_vars(client.me.id, "ADMIN_USERS")
    if user_id not in admin_list:
        return await callback_query.answer("Ini bukan buat kamu!", show_alert=True)
    await callback_query.answer("⌬ Sistem berhasil direstart!", show_alert=True)
    subprocess.call(["bash", "start.sh"])


@PY.CALLBACK("update")
async def update_callback(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id != OWNER_ID:
        return await callback_query.answer("Ini bukan buat kamu!", show_alert=True)
    out = subprocess.check_output(["git", "pull"]).decode("UTF-8")
    if "Already up to date." in out:
        return await callback_query.answer("⌬ Sudah versi terbaru!", show_alert=True)
    await callback_query.answer("⟳ Lagi proses update...", show_alert=True)
    os.execl(sys.executable, sys.executable, "-m", "PyroUbot")



@PY.UBOT("help")
async def user_help(client, message):
    if not get_arg(message):
        try:
            x = await client.get_inline_bot_results(bot.me.username, "user_help")
            await message.reply_inline_bot_result(x.query_id, x.results[0].id)
        except Exception as error:
            await message.reply(f"<blockquote><b>⌭ Error:</b> {error}</blockquote>")
    else:
        module = get_arg(message)
        if module in HELP_COMMANDS:
            prefix = await ubot.get_prefix(client.me.id)
            await message.reply(
                HELP_COMMANDS[module].__HELP__.format(next((p) for p in prefix)),
                quote=True,
            )
        else:
            await message.reply(f"<blockquote><b>⌭ Modul <code>{module}</code> ga ketemu!</b></blockquote>")


@PY.INLINE("^user_help")
async def user_help_inline(client, inline_query):
    SH = await ubot.get_prefix(inline_query.from_user.id)

    caption = (
        f"<blockquote><b>◆ Menu Help RANZ PEDIA</b>\n\n"
        f"<b>User:</b> <a href='tg://user?id={inline_query.from_user.id}'>"
        f"{inline_query.from_user.first_name} {inline_query.from_user.last_name or ''}</a>\n"
        f"<b>Total Modul:</b> {len(HELP_COMMANDS)}\n"
        f"<b>Prefix:</b> {' '.join(SH)}\n"
        f"<b>Bot:</b> <a href='t.me/{bot.me.username}'>{bot.me.username}</a></blockquote>"
    )

    results = [
        InlineQueryResultPhoto(
            photo_url="https://i.imgur.com/7BTzIeo.png",
            thumb_url="https://i.imgur.com/7BTzIeo.png",
            caption=caption,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(0, HELP_COMMANDS, "help")
            ),
        )
    ]

    await client.answer_inline_query(
        inline_query.id,
        cache_time=60,
        results=results,
    )


@PY.CALLBACK("^close_user")
async def close_user_callback(client, callback_query):
    unPacked = unpackInlineMessage(callback_query.inline_message_id)
    for x in ubot._ubot:
        if callback_query.from_user.id == int(x.me.id):
            await x.delete_messages(unPacked.chat_id, unPacked.message_id)


@PY.CALLBACK("help_(.*?)")
async def help_callback(client, callback_query):
    mod_match = re.match(r"help_module\((.+?)\)", callback_query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", callback_query.data)
    next_match = re.match(r"help_next\((.+?)\)", callback_query.data)
    back_match = re.match(r"help_back", callback_query.data)
    SH = await ubot.get_prefix(callback_query.from_user.id)

    top_text = (
        f"<blockquote><b>◆ Menu Help RANZ PEDIA</b>\n\n"
        f"<b>User:</b> <a href='tg://user?id={callback_query.from_user.id}'>"
        f"{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}</a>\n"
        f"<b>Total Modul:</b> {len(HELP_COMMANDS)}\n"
        f"<b>Prefix:</b> {' '.join(SH)}\n"
        f"<b>Bot:</b> <a href='t.me/{bot.me.username}'>{bot.me.username}</a></blockquote>"
    )

    if mod_match:
        module = mod_match.group(1).replace(" ", "_")
        text = HELP_COMMANDS[module].__HELP__.format(next((p) for p in SH))
        button = [[InlineKeyboardButton("← Kembali", callback_data="help_back")]]
        await callback_query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(button),
            disable_web_page_preview=True,
        )
    elif prev_match:
        curr_page = int(prev_match.group(1))
        await callback_query.edit_message_text(
            top_text,
            reply_markup=InlineKeyboardMarkup(paginate_modules(curr_page - 1, HELP_COMMANDS, "help")),
            disable_web_page_preview=True,
        )
    elif next_match:
        next_page = int(next_match.group(1))
        await callback_query.edit_message_text(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(paginate_modules(next_page + 1, HELP_COMMANDS, "help")),
            disable_web_page_preview=True,
        )
    elif back_match:
        await callback_query.edit_message_text(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(paginate_modules(0, HELP_COMMANDS, "help")),
            disable_web_page_preview=True,
        )
