import aiohttp
from PyroUbot import *

__MODULE__ = "ᴘɪɴᴛᴇʀᴇsᴛ"
__HELP__ = """
<blockquote><b>Pinterest</b></b>

<b>Perintah:</b>
<code>{0}pin</code> [link] → Download foto/video dari Pinterest.</blockquote></b>
"""

@PY.UBOT("pin")
@PY.TOP_CMD
async def _(client, message):
    if len(message.command) < 2:
        return await message.reply_text("<blockquote>Ketik <code>.pin [link]</code></blockquote>")

    link = message.text.split(None, 1)[1]
    status = await message.reply_text("<blockquote><b>⌛ Memproses Pinterest...</b></blockquote>")

    async with aiohttp.ClientSession() as session:
        try:
            api_url = f"https://api.botcahx.eu.org/api/dowloader/pinterest?url={link}&apikey=@31Moire_mor"
            async with session.get(api_url) as resp:
                data = await resp.json()

            if not data.get("status") or "result" not in data:
                return await status.edit("<blockquote><b>⌭ gagal!</b> Link tidak valid atau API sedang maintenance.</blockquote>")

            res = data["result"]
            # Pinterest bisa berupa foto atau video
            if res.get("type") == "video":
                await client.send_video(message.chat.id, res["url"], caption="<blockquote>⌬ <b>Video Pinterest Berhasil Diunduh</b></blockquote>")
            else:
                await client.send_photo(message.chat.id, res["url"], caption="<blockquote>⌬ <b>Foto Pinterest Berhasil Diunduh</b></blockquote>")
            
            await status.delete()
        except Exception as e:
            await status.edit(f"<blockquote><b>⌯ Error:</b> <code>{str(e)}</code></blockquote>")
            