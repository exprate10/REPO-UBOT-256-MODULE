from PyroUbot import *
import random
import requests
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters
from pyrogram.types import Message

__MODULE__ = "ᴇɴᴄ ʙᴀsᴇ64"
__HELP__ = """
<b>⦪ <blockquote>⎆ <b>Perintah:</b>
ᚗ <code>{0}enc64</code> code
⊶ untuk encode base64.
</blockquote>
"""

@PY.UBOT("enc64")
@PY.TOP_CMD
async def chat_gpt(client, message):
    try:
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)

        if len(message.command) < 2:
            await message.reply_text(
                "<emoji id=5019523782004441717>⌭</emoji>tolong gunakan format\ncontoh : .enc64 [code]"
            )
        else:
            prs = await message.reply_text(f"<emoji id=6298414727487818323>😉</emoji>proccesing encode base64....")
            a = message.text.split(' ', 1)[1]
            response = requests.get(f'https://vapis.my.id/api/tobase64?q={a}')

            try:
                if "result" in response.json():
                    x = response.json()["result"]                  
                    await prs.edit(
                      f"<blockquote>`{x}`</blockquote>"
                    )
                else:
                    await message.reply_text("No 'results' key found in the response.")
            except KeyError:
                await message.reply_text("Error accessing the response.")
    except Exception as e:
        await message.reply_text(f"{e}")
