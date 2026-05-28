import os
from PIL import Image, ImageDraw, ImageFont, ImageOps
from pyrogram import Client
from pyrogram.types import User, Chat
from PyroUbot import *

__MODULE__ = "ᴄᴇᴋ ɪᴅ"
__HELP__ = """
<b>⦪ <blockquote>⎆ <b>Perintah:</b>
ᚗ <code>{0}cekid</code>
⊶ Untuk Mengambil Data User/Channel/Grup.
</blockquote>
"""

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DEFAULT_PROFILE_PATH = "storage/default.jpg"


def download_image():
    if os.path.exists(DEFAULT_PROFILE_PATH):
        return Image.open(DEFAULT_PROFILE_PATH).convert("RGBA").resize((140, 140))
    return None


async def generate_profile_card(client: Client, user: User):

    os.makedirs("downloads", exist_ok=True)
    os.makedirs("storage", exist_ok=True)

    width, height = 800, 400
    img = Image.new("RGB", (width, height), (30, 30, 40))
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle(
        [(20, 20), (780, 380)],
        radius=30,
        fill=(50, 50, 70)
    )

    profile_size = 140
    profile_x, profile_y = 60, 130

    profile_photo_path = f"downloads/profile_{user.id}.jpg"

    profile_photo = None

    try:
        async for photo in client.get_chat_photos(user.id, limit=1):
            await client.download_media(photo.file_id, file_name=profile_photo_path)
            break
    except:
        pass

    if os.path.exists(profile_photo_path):
        profile_photo = Image.open(profile_photo_path).convert("RGBA").resize(
            (profile_size, profile_size)
        )
    else:
        profile_photo = download_image()

    if profile_photo:

        mask = Image.new("L", (profile_size, profile_size), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, profile_size, profile_size), fill=255)

        profile_photo = ImageOps.fit(
            profile_photo,
            (profile_size, profile_size)
        )

        profile_photo.putalpha(mask)

        img.paste(
            profile_photo,
            (profile_x, profile_y),
            profile_photo
        )

    font_title = ImageFont.truetype(FONT_PATH, 36)
    font_text = ImageFont.truetype(FONT_PATH, 24)

    draw.text(
        (230, 40),
        "TELEGRAM ID CARD",
        font=font_title,
        fill=(255, 220, 100)
    )

    first_name = user.first_name or "Pengguna"
    username_text = f"@{user.username}" if user.username else "ga ada"
    dc_id = user.dc_id or "Tidak diketahui"
    premium = "Iya" if getattr(user, "is_premium", False) else "Tidak"

    details = [
        ("Nama", first_name),
        ("User ID", str(user.id)),
        ("Username", username_text),
        ("DC ID", str(dc_id)),
        ("Premium", premium),
    ]

    y_text = 100

    for label, value in details:

        label_text = f"{label}:"
        value_text = str(value)

        draw.text(
            (230, y_text),
            label_text,
            font=font_text,
            fill=(200, 200, 200)
        )

        label_width = draw.textlength(
            label_text,
            font=font_text
        )

        draw.text(
            (230 + label_width + 20, y_text),
            value_text,
            font=font_text,
            fill=(173, 216, 230)
        )

        y_text += 50

    final_path = f"downloads/card_{user.id}.jpg"

    img.save(final_path, "JPEG")

    if os.path.exists(profile_photo_path):
        os.remove(profile_photo_path)

    return final_path


@PY.UBOT("id|cekid")
async def cekidte(client, message):

    target_user = message.from_user

    if message.reply_to_message:
        if message.reply_to_message.from_user:
            target_user = message.reply_to_message.from_user

    if len(message.text.split()) > 1:
        try:
            target_user = await client.get_users(
                message.text.split()[1]
            )
        except:
            return await message.reply(
                "<b>⌭ Pengguna ga ketemu</b>"
            )

    wait = await message.reply("◷ sebentar ya...")

    card = await generate_profile_card(
        client,
        target_user
    )

    name_link = f'<a href="tg://user?id={target_user.id}">{target_user.first_name}</a>'

    chat_title = (
        message.chat.title
        if isinstance(message.chat, Chat)
        else "Private"
    )

    username_text = (
        f"@{target_user.username}"
        if target_user.username
        else "ga ada"
    )

    caption = f"""
<blockquote><b>╭──「 ⌖ NI BRO DATA BELIAU YG SANGAT BAPERAN 🗿」</b>
│ ◉ <b>Nama:</b> {name_link}
│ 🟢 <b>ID:</b> <code>{target_user.id}</code>
│ 🔱 <b>Username:</b> {username_text}
│ ◈ <b>DC:</b> <code>{target_user.dc_id or 'Tidak diketahui'}</code>
│ ✨️ <b>Premium:</b> {"Premium ⌬" if getattr(target_user,'is_premium',False) else "Tidak ⌭"}
│ 🆔 <b>Chat ID:</b> <code>{message.chat.id}</code> ({chat_title})
│ ⌕ <b>Link:</b> <a href="tg://user?id={target_user.id}">Klik</a>
╰──「 <b>@UbotRanzxyBot</b> 」</blockquote>
"""

    await wait.delete()

    await message.reply_photo(
        card,
        caption=caption
    )

    os.remove(card)