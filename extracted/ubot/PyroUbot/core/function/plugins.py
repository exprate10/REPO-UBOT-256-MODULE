import importlib
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from PyroUbot import bot, ubot
from PyroUbot.core.helpers import PY
from PyroUbot.modules import loadModule
from PyroUbot.core.database import *
from PyroUbot.config import OWNER_ID
from platform import python_version
from pyrogram import __version__

HELP_COMMANDS = {}


async def loadPlugins():
    modules = loadModule()
    for mod in modules:
        imported_module = importlib.import_module(f"PyroUbot.modules.{mod}")
        module_name = getattr(imported_module, "__MODULE__", "").replace(" ", "_").lower()
        if module_name:
            HELP_COMMANDS[module_name] = imported_module

    print(f"[🤖 @{bot.me.username} 🤖] [💠 RANZ PEDIA ONLINE 💠]")

    await bot.send_message(
        OWNER_ID,
        f"<blockquote><b>✅ {bot.me.mention} Berhasil Diaktifkan!</b>\n\n"
        f"<b>📦 Modul:</b> {len(HELP_COMMANDS)}\n"
        f"<b>🐍 Python:</b> {python_version()}\n"
        f"<b>📱 Pyrogram:</b> {__version__}\n"
        f"<b>🤖 Userbot Aktif:</b> {len(ubot._ubot)}</blockquote>",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("📋 List Userbot", callback_data="cek_ubot"),
        ]]),
    )


@PY.CALLBACK("0_cls")
async def cls_callback(client, callback_query):
    await callback_query.message.delete()
