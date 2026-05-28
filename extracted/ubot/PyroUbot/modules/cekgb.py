import asyncio
from pyrogram import enums
from PyroUbot import *

__MODULE__ = "ᴄʜᴇᴄᴋ ɢʙ"
__HELP__ = """
<blockquote><b>Bantuan Untuk Cek GB Quote</b>

<b>Perintah:</b>
<code>{0}cekgb</code> [halaman]
Contoh: <code>.cekgb 2</code>
<i>(Tampilan rapi di dalam kutipan & auto-edit)</i></blockquote></b>
"""

@PY.UBOT("cekgb")
@PY.TOP_CMD
async def _(client, message):
    # Kirim status awal
    status = await message.reply_text("<blockquote><b>🔍 Sedang menyisir grup...</b></blockquote>")
    
    group_list = []
    async for dialog in client.get_dialogs():
        if dialog.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            group_list.append({
                "title": dialog.chat.title,
                "id": dialog.chat.id,
                "user": f"@{dialog.chat.username}" if dialog.chat.username else "Private Group"
            })

    if not group_list:
        return await status.edit("<blockquote><b>❌ Waduh, kamu belum join grup manapun.</b></blockquote>")

    # Konfigurasi Halaman
    per_page = 10 
    total_gb = len(group_list)
    total_pages = (total_gb - 1) // per_page + 1
    
    args = message.command
    page = int(args[1]) if len(args) > 1 and args[1].isdigit() else 1
    
    if page > total_pages or page < 1:
        return await status.edit(f"<blockquote><b>❌ Halaman {page} tidak ada!</b>\nTotal: {total_pages} Halaman.</blockquote>")

    start = (page - 1) * per_page
    end = start + per_page
    current_page_list = group_list[start:end]

    # --- MULAI BUILD TEKS KUTIPAN ---
    res = f"<blockquote><b>📁 DAFTAR GRUP JOINED</b>\n"
    res += f"<b>Total:</b> <code>{total_gb}</code> <b>Grup</b>\n"
    res += f"<b>Halaman:</b> <code>{page}/{total_pages}</code>\n"
    res += "━━━━━━━━━━━━━━━━━━\n\n"

    for i, g in enumerate(current_page_list, start=start + 1):
        res += f"<b>{i}. {g['title']}</b>\n"
        res += f"┣ <code>{g['id']}</code>\n"
        res += f"┗ <b>Link:</b> {g['user']}\n\n"

    # Navigasi di dalam kutipan biar estetik
    res += "<b>───[ NAVIGASI ]───</b>\n"
    nav = []
    if page > 1:
        nav.append(f"<code>.cekgb {page - 1}</code> ⬅️")
    if page < total_pages:
        nav.append(f"➡️ <code>.cekgb {page + 1}</code>")
    
    res += " | ".join(nav) if nav else "<i>Halaman Terakhir</i>"
    res += "</blockquote>"

    # Hapus pesan perintah asli user
    try:
        await message.delete()
    except:
        pass

    # Edit pesan menjadi tampilan kutipan
    await status.edit(res)
    