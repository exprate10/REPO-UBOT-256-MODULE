import asyncio
import random
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message

# Mengimpor PY.UBOT dan PY.TOP_CMD dari modul PyroUbot harus disesuaikan dengan cara impor yang benar.
from PyroUbot import *



__MODULE__ = "ᴀɴɪᴍᴀsɪ 2"
__HELP__ = """
<b>⦪ 
<blockqoute><b>⎆ <b>Perintah:</b>
ᚗ <code>{0}dino</code> 
ᚗ <code>{0}hack</code> 
ᚗ <code>{0}gabut</code> 
ᚗ <code>{0}loveyou</code> 
ᚗ <code>{0}bomb</code> 
ᚗ <code>{0}charge</code></b></blockqoute>
"""


SLEEP = 1

@PY.UBOT("loveyou")
@PY.TOP_CMD
async def hearts(client: Client, message: Message):
    await asyncio.sleep(SLEEP * 3)
    await message.edit("❤️ I")
    await asyncio.sleep(0.5)
    await message.edit("❤️ I Love")
    await asyncio.sleep(0.5)
    await message.edit("❤️ I Love You")
    await asyncio.sleep(3)
    await message.edit("❤️ I Love You <3")

@PY.UBOT("bomb")
@PY.TOP_CMD
async def gahite(client: Client, message: Message):
    if message.forward_from:
        return
    for i in range(5):
        await message.edit("▪️▪️▪️▪️ \n" * (i) + "💣💣💣💣 \n" + "▪️▪️▪️▪️ \n" * (4-i))
        await asyncio.sleep(0.5)
    await message.edit("▪️▪️▪️▪️ \n" * 4 + "💥💥💥💥 \n")
    await asyncio.sleep(0.5)
    await message.edit("▪️▪️▪️▪️ \n" * 3 + "💥💥💥💥 \n" * 2)
    await asyncio.sleep(0.5)
    await message.edit("▪️▪️▪️▪️ \n" * 4 + "😵😵😵😵 \n")
    await asyncio.sleep(0.5)
    await message.edit("`RIP PLOXXX......`")
    await asyncio.sleep(2)

@PY.UBOT("charge")
@PY.TOP_CMD
async def timer_blankx(client: Client, msg: Message):
    txt = (
        msg.text[8:]
        + "\n\n`Tesla Wireless Charging (beta) Started...\nDevice Detected: Nokia 1100\nBattery Percentage:` "
    )
    for j in range(10, 101, 10):
        await msg.edit_text(txt + str(j))
        await asyncio.sleep(1)
    await asyncio.sleep(1)
    await msg.edit_text(
        "`Tesla Wireless Charging (beta) Completed...\nDevice Detected: Nokia 1100 (Space Grey Varient)\nBattery Percentage:` [100%](https://telegra.ph/file/a45aa7450c8eefed599d9.mp4)",
        disable_web_page_preview=False,
    )

@PY.UBOT("hack")
@PY.TOP_CMD
async def hak(client: Client, message: Message):
    hacking_steps = [
        ("Looking for Telegram databases in targeted person...", 2),
        (" User online: True\nTelegram access: True\nRead Storage: True ", 2),
        ("Hacking... 0%\n[░░░░░░░░░░░░░░░░░░░░]\n`Looking for Telegram...`\nETA: 0m, 20s", 2),
        ("Hacking... 11.07%\n[██░░░░░░░░░░░░░░░░░░]\n`Looking for Telegram...`\nETA: 0m, 18s", 2),
        ("Hacking... 20.63%\n[███░░░░░░░░░░░░░░░░░]\n`Found folder C:/Telegram`\nETA: 0m, 16s", 2),
        ("Hacking... 34.42%\n[█████░░░░░░░░░░░░░░░]\n`Found folder C:/Telegram`\nETA: 0m, 14s", 2),
        ("Hacking... 42.17%\n[███████░░░░░░░░░░░░░]\n`Searching for databases`\nETA: 0m, 12s", 2),
        ("Hacking... 55.30%\n[█████████░░░░░░░░░░░]\n`Found msgstore.db.crypt12`\nETA: 0m, 10s", 2),
        ("Hacking... 64.86%\n[███████████░░░░░░░░░]\n`Found msgstore.db.crypt12`\nETA: 0m, 08s", 2),
        ("Hacking... 74.02%\n[█████████████░░░░░░░]\n`Trying to Decrypt...`\nETA: 0m, 06s", 2),
        ("Hacking... 86.21%\n[███████████████░░░░░]\n`Trying to Decrypt...`\nETA: 0m, 04s", 2),
        ("Hacking... 93.50%\n[█████████████████░░░]\n`Decryption successful!`\nETA: 0m, 02s", 2),
        ("Hacking... 100%\n[████████████████████]\n`Scanning file...`\nETA: 0m, 00s", 2),
        ("Hacking complete!\nUploading file...", 2),
        ("Targeted Account Hacked...!\n\n ⌬ File has been successfully uploaded to my server.\nTelegram Database:\n`./DOWNLOADS/msgstore.db.crypt12`", 2),
    ]
    for step, delay in hacking_steps:
        await message.edit(step)
        await asyncio.sleep(delay)


# Define the edit_or_reply function
async def edit_or_reply(message: Message, text: str):
    if message.from_user.is_self:
        return await message.edit_text(text)
    else:
        return await message.reply_text(text)

@PY.UBOT("dino")
@PY.TOP_CMD
async def adadino(client: Client, message: Message):
    typew = await edit_or_reply(message, "`DIN DINNN.....`")
    await asyncio.sleep(1)
    await typew.edit("`DINOOOOSAURUSSSSS!!`")
    await asyncio.sleep(1)

    dino_chase_frames = [
        "`🏃                        🦖`",
        "`🏃                       🦖`",
        "`🏃                      🦖`",
        "`🏃                     🦖`",
        "`🏃   `Lari uus`          🦖`",
        "`🏃                   🦖`",
        "`🏃                  🦖`",
        "`🏃                 🦖`",
        "`🏃                🦖`",
        "`🏃               🦖`",
        "`🏃              🦖`",
        "`🏃             🦖`",
        "`🏃            🦖`",
        "`🏃           🦖`",
        "`🏃WOARGH!   🦖`",
        "`🏃           🦖`",
        "`🏃            🦖`",
        "`🏃             🦖`",
        "`🏃              🦖`",
        "`🏃               🦖`",
        "`🏃                🦖`",
        "`🏃                 🦖`",
        "`🏃                  🦖`",
        "`🏃                   🦖`",
        "`🏃                    🦖`",
        "`🏃                     🦖`",
        "`🏃  Huh-Huh           🦖`",
        "`🏃                   🦖`",
        "`🏃                  🦖`",
        "`🏃                 🦖`",
        "`🏃                🦖`",
        "`🏃               🦖`",
        "`🏃              🦖`",
        "`🏃             🦖`",
        "`🏃            🦖`",
        "`🏃           🦖`",
        "`🏃          🦖`",
        "`🏃         🦖`",
        "`HE WAS GETTING CLOSER!!!`",
        "`🏃       🦖`",
        "`🏃      🦖`",
        "`🏃     🦖`",
        "`🏃    🦖`",
        "`Just give up`",
        "`🧎🦖`",
        "`-DIED-`"
    ]

    for frame in dino_chase_frames:
        await typew.edit(frame)
        await asyncio.sleep(0.5)

@PY.UBOT("gabut")
@PY.TOP_CMD
async def menggabut(client: Client, message: Message):
    e = await edit_or_reply(message, "`GABUT`")
    await asyncio.sleep(1)
    
    gabut_frames = [
        "`G A B U T`",
        "`G  A  B  U  T`",
        "`G   A   B   U   T`",
        "`G    A    B    U    T`",
        "`G   A   B   U   T`",
        "`G  A  B  U  T`",
        "`G A B U T`",
        "`GABUT`",
        "🙈🙈🙈🙈",
        "🙉🙉🙉🙉",
        "🙈🙈🙈🙈",
        "🙉🙉🙉🙉",
        "`GABUT NJINK`",
        "🙉🙉🙉🙉",
        "🐢                       🚶",
        "🐢                      🚶",
        "🐢                     🚶",
        "🐢                    🚶",
        "🐢                   🚶",
        "🐢                  🚶",
        "🐢                 🚶",
        "🐢                🚶",
        "🐢               🚶",
        "🐢              🚶",
        "🐢             🚶",
        "🐢            🚶",
        "🐢           🚶",
        "🐢          🚶",
        "🐢         🚶",
        "🐢        🚶",
        "🐢       🚶",
        "🐢      🚶",
        "🐢     🚶",
        "🐢    🚶",
        "🐢   🚶",
        "🐢  🚶",
        "🐢 🚶",
        "🐢🚶",
        "🚶🐢",
        "🚶 🐢",
        "🚶  🐢",
        "🚶   🐢",
        "🚶    🐢",
        "🚶     🐢",
        "🚶      🐢",
        "🚶       🐢",
        "🚶        🐢",
        "🚶         🐢",
        "🚶          🐢",
        "🚶           🐢",
        "🚶            🐢",
        "🚶             🐢",
        "🚶              🐢",
        "🚶               🐢",
        "🚶                🐢",
        "🚶                 🐢",
        "🚶                  🐢",
        "🚶                   🐢",
        "🚶                    🐢",
        "🚶                     🐢",
        "🚶                      🐢",
        "🚶                       🐢",
        "🚶                        🐢",
        "🚶                         🐢",
        "🚶                          🐢",
        "🚶                           🐢",
        "🚶                            🐢",
        "🚶                             🐢",
        "🚶                              🐢",
        "🚶                               🐢",
        "🚶                                🐢",
        "`GABUT NJIR`",
        "🙉",
        "🙈",
        "🙉",
        "🙈",
        "🙉",
        "",
        "🐢                       🚶",
        "🐢                      🚶",
        "🐢                     🚶",
        "🐢                    🚶",
        "🐢                   🚶",
        "🐢                  🚶",
        "🐢                 🚶",
        "🐢                🚶",
        "🐢               🚶",
        "🐢              🚶",
        "🐢             🚶",
        "🐢            🚶",
        "🐢           🚶",
        "🐢          🚶",
        "🐢         🚶",
        "🐢        🚶",
        "🐢       🚶",
        "🐢      🚶",
        "🐢     🚶",
        "🐢    🚶",
        "🐢   🚶",
        "🐢  🚶",
        "🐢 🚶",
        "🐢🚶",
        "🚶🐢",
        "🚶 🐢",
        "🚶  🐢",
        "🚶   🐢",
        "🚶    🐢",
        "🚶     🐢",
        "🚶      🐢",
        "🚶       🐢",
        "🚶        🐢",
        "🚶         🐢",
        "🚶          🐢",
        "🚶           🐢",
        "🚶            🐢",
        "🚶             🐢",
        "🚶              🐢",
        "🚶               🐢",
        "🚶                🐢",
        "🚶                 🐢",
        "🚶                  🐢",
        "🚶                   🐢",
        "🚶                    🐢",
        "🚶                     🐢",
        "🚶                      🐢",
        "🚶                       🐢",
        "🚶                        🐢",
        "🚶                         🐢",
        "🚶                          🐢",
        "🚶                           🐢",
        "🚶                            🐢",
        "🚶                             🐢",
        "🚶                              🐢",
        "🚶                               🐢",
        "🚶                                🐢",
        "`GABUT`"
    ]

    for frame in gabut_frames:
        await e.edit(frame)
        await asyncio.sleep(0.3)
