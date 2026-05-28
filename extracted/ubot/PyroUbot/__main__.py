import asyncio
import os
import sys
import signal
import tornado.ioloop
import tornado.platform.asyncio
from datetime import datetime
from pyrogram import Client, filters
from PyroUbot import *
from PyroUbot.config import LOGS_MAKER_UBOT


@bot.on_message(filters.command("restart"))
async def restart_bot_handler(client, message):
    pengirim_name = message.from_user.first_name
    pengirim_id = message.from_user.id

    status = await message.reply(
        "<blockquote><b>⏳ Lagi restart, tunggu sebentar...</b></blockquote>"
    )

    await asyncio.sleep(2)

    await status.edit(
        f"<blockquote><b>✅ Restart Berhasil!</b>\n\n"
        f"<b>Oleh:</b> {pengirim_name} | <code>{pengirim_id}</code></blockquote>"
    )

    os.execl(sys.executable, sys.executable, "-m", "PyroUbot")


async def shutdown(signal, loop):
    print(f"Received exit signal {signal.name}...")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    print("Cancelling outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()


async def send_log_startup():
    await asyncio.sleep(5)

    if ubot._ubot:
        akun_utama = ubot._ubot[0]
        try:
            text_start = (
                f"<blockquote><b>🟢 RANZ PEDIA — Userbot Aktif</b>\n\n"
                f"<b>Akun:</b> {akun_utama.me.first_name}\n"
                f"<b>ID:</b> <code>{akun_utama.me.id}</code></blockquote>"
            )
            await bot.send_message(LOGS_MAKER_UBOT, text_start)
        except Exception as e:
            print(f"Gagal kirim log ke CH: {e}")


async def main():
    await bot.start()

    try:
        await bot.send_message(
            LOGS_MAKER_UBOT,
            f"<blockquote><b>🤖 RANZ PEDIA Bot Started</b>\n\n"
            f"<b>⏰ Waktu:</b> {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n"
            f"<b>✅ Status:</b> Online</blockquote>"
        )
    except Exception:
        pass

    for _ubot in await get_userbots():
        ubot_ = Ubot(**_ubot)
        try:
            await asyncio.wait_for(ubot_.start(), timeout=10)

            try:
                await bot.send_message(
                    LOGS_MAKER_UBOT,
                    f"<blockquote><b>🚀 Userbot Aktif</b>\n\n"
                    f"<b>Akun:</b> {ubot_.me.first_name}\n"
                    f"<b>ID:</b> <code>{ubot_.me.id}</code></blockquote>"
                )
            except Exception:
                pass

        except asyncio.TimeoutError:
            await remove_ubot(int(_ubot["name"]))
            print(f"[INFO]: {int(_ubot['name'])} tidak bisa merespon, dihapus")
        except Exception:
            await remove_ubot(int(_ubot["name"]))
            print(f"[INFO]: {int(_ubot['name'])} gagal start, dihapus")

    await bash("rm -rf *session*")

    await asyncio.gather(loadPlugins(), installPeer(), expiredUserbots())

    asyncio.create_task(send_log_startup())

    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()
    for s in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(
            s, lambda: asyncio.create_task(shutdown(s, loop))
        )

    try:
        await stop_event.wait()
    except asyncio.CancelledError:
        pass
    finally:
        await bot.stop()


if __name__ == "__main__":
    tornado.platform.asyncio.AsyncIOMainLoop().install()
    loop = tornado.ioloop.IOLoop.current().asyncio_loop
    loop.run_until_complete(main())
