from PyroUbot import *
import os
import json
import asyncio
import psutil
import random
import requests
import re
import platform
import subprocess
import sys
import traceback
import aiohttp
import filetype
import wget
import math

from datetime import datetime
from io import BytesIO, StringIO
from PyroUbot.config import OWNER_ID
from pyrogram.enums import UserStatus
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import ChatAdminRequired, UserBannedInChannel
from pytgcalls import PyTgCalls
from youtubesearchpython import VideosSearch
from pyrogram.enums import ChatType, ChatAction, ParseMode
from httpx import AsyncClient, Timeout

__MODULE__ = "ᴏɴɢɴᴇʀ"
__HELP__ = """
<blockquote><b>ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴏɴɢɴᴇʀ</b></blockquote>

<blockquote><b>ᴘᴇʀɪɴᴛᴀʜ : <code>{0}ᴄᴘɪɴɢ</code> - <code>{0}ᴄᴀᴅᴅʙʟ</code> - <code>{0}ᴄʟɪᴍɪᴛ</code> - <code>ᴄᴀʟɪᴠᴇ</code></b></blockquote>

<blockquote><b>ᴘᴇʀɪɴᴛᴀʜ : <code>{0}ʙᴏʏsᴢ ɢᴀɴᴛᴇɴᴋ ɢᴀ</code> - <code>{0}ᴛᴇs ᴏɴ</code></b></blockquote>

<blockquote><b>- <code>{0}ᴘ</code>\n- <code>{0}ᴏᴋ</code>\n- <code>{0}sɪᴘ</code>\n- <code>{0}ʟᴏᴠᴇ</code>\n- <code>{0}ʜᴀʜᴀ</code>\n- <code>{0}ᴋᴜᴅᴀ</code></b></blockquote>
"""
    
@PY.INDRI("pada on ga")
async def padaonga(client, message):
    await message.reply(
        "‡‡‡‡‡‡‡‡‡‡‡‡▄▄▄▄\n"
        "‡‡‡‡‡‡‡‡‡‡‡█‡‡‡‡█\n"
        "‡‡‡‡‡‡‡‡‡‡‡█‡‡‡‡█\n"
        "‡‡‡‡‡‡‡‡‡‡█‡‡‡‡‡█\n"
        "‡‡‡‡‡‡‡‡‡█‡‡‡‡‡‡█\n"
        "██████▄▄█‡‡‡‡‡‡████████▄\n"
        "▓▓▓▓▓▓█‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡█\n"
        "▓▓▓▓▓▓█‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡█\n"
        "▓▓▓▓▓▓█‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡█\n"
        "▓▓▓▓▓▓█‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡█\n"
        "▓▓▓▓▓▓█‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡‡█\n"
        "▓▓▓▓▓▓█████‡‡‡‡‡‡‡‡‡‡‡‡██\n"
        "█████‡‡‡‡‡‡‡██████████\n")
    
@PY.INDRI("boysz gantenk ga")
async def didingantenkga(client, message):
    await message.reply(
       "<blockquote><b>ʏᴀ ʙᴇɴᴀʀ ᴅɪᴀ sᴀɴɢᴀᴛ ɢᴀɴᴛᴇɴᴋ sᴇᴋᴀʟɪ\n\n- ᴅɪᴀ ʙᴀɪᴋ\n- ᴅɪᴀ ᴍᴀɴɪs\n- ᴅɪᴀ ʟᴜᴄᴜ\n- ᴅɪᴀ ɪᴍᴜᴛ\n- ᴅɪᴀ ᴋᴏɴʙʀᴜᴛ ᴀᴡsᴊsʜsᴊʜsᴊs\n\nɪᴅᴀᴍᴀɴ ʙᴀɴɢᴇᴛ ʟᴀʜ ᴘᴏᴋᴏɴʏᴀ ʙᴏʏsᴢ ɴɪʜ</b></blockquote>")

@PY.INDRI("tes on")
async def teson(client, message):
    await message.reply(
       "<blockquote><b>ᴏɴ sᴇʟᴀʀᴜ ᴅᴇᴠ ᴋɪɴɢᴢ👑</b></blockquote>")
        
@PY.INDRI("kuda")
async def _(client, message):
    try: await message.react("🦄")
    except: pass

@PY.INDRI("love")
async def _(client, message):
    try: await message.react("❤")
    except: pass

@PY.INDRI("sip")
async def _(client, message):
    try: await message.react("👍")
    except: pass

@PY.INDRI("ok")
async def _(client, message):
    try: await message.react("👌")
    except: pass

@PY.INDRI("haha")
async def _(client, message):
    try: await message.react("😹")
    except: pass

@PY.INDRI("p")
async def _(client, message):
    try: await message.react("👋")
    except: pass

@PY.INDRI("wow")
async def _(client, message):
    try: await message.react("😨")
    except: pass
    
