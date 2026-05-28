import os
import httpx
from PyroUbot import *

__MODULE__ = "ɢᴛᴛs"
__HELP__ = """
<blockquote><b>♛ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ɢᴛᴛs ♛</b>

<b>Perintah:</b>
• <code>.tts</code> [teks]
ᴍᴇɴɢᴜʙᴀʜ ᴛᴇᴋs ᴍᴇɴᴊᴀᴅɪ sᴜᴀʀᴀ (ɢᴏᴏɢʟᴇ ᴠᴏɪᴄᴇ).

<b>Pᴇɴᴊᴇʟᴀsᴀɴ:</b> sᴜᴀʀᴀ ᴅᴇғᴀᴜʟᴛ ᴀᴅᴀʟᴀʜ ʙᴀʜᴀsᴀ ɪɴᴅᴏɴᴇsɪᴀ.</blockquote>
"""

@PY.UBOT("tts")
async def gtts_cmd(client, message):
    if len(message.command) < 2:
        return await message.reply("<blockquote>❌ <b>ʜᴀʀᴀᴘ ᴍᴀsᴜᴋᴋᴀɴ ᴛᴇᴋs!</b>\nᴄᴏɴᴛᴏʜ: <code>.tts halo bosqu</code></blockquote>")

    teks = message.text.split(None, 1)[1]
    sh = await message.reply("<b>sᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏsᴇs...</b>")
    
    # API Google TTS yang ringan
    tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={teks.replace(' ', '%20')}&tl=id&client=tw-ob"
    
    try:
        async with httpx.AsyncClient() as x:
            res = await x.get(tts_url)
            if res.status_code != 200:
                return await sh.edit("<blockquote>❌ <b>ɢᴀɢᴀʟ ᴍᴇɴɢᴀᴍʙɪʟ sᴜᴀʀᴀ.</b></blockquote>")
            
            audio_data = res.content
            
        file_name = f"tts_{message.id}.mp3"
        with open(file_name, "wb") as f:
            f.write(audio_data)
            
        await client.send_voice(
            message.chat.id,
            voice=file_name,
            caption=f"<blockquote>🗣️ <b>ᴛᴇᴋs:</b> <code>{teks}</code></blockquote>",
            reply_to_message_id=message.id
        )
        await sh.delete()
        if os.path.exists(file_name):
            os.remove(file_name)
            
    except Exception as e:
        await sh.edit(f"<blockquote>❌ ᴇʀʀᴏʀ: <code>{str(e)}</code></blockquote>")

