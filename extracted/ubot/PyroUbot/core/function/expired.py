import asyncio
from datetime import datetime

from pyrogram.types import InlineKeyboardMarkup
from pytz import timezone

from PyroUbot import *


async def expiredUserbots():
    while True:
        for X in list(ubot._ubot):
            try:
                time_now = datetime.now(timezone("Asia/Jakarta")).strftime("%d-%m-%Y")
                exp = await get_expired_date(X.me.id)
                if exp is None:
                    continue
                exp_str = exp.strftime("%d-%m-%Y")
                if time_now == exp_str:
                    await X.unblock_user(bot.me.username)
                    await remove_ubot(X.me.id)
                    await remove_all_vars(X.me.id)
                    await rem_expired_date(X.me.id)
                    if X.me.id in ubot._get_my_id:
                        ubot._get_my_id.remove(X.me.id)
                    if X in ubot._ubot:
                        ubot._ubot.remove(X)
                    await X.log_out()

                    from PyroUbot.core.helpers.text import MSG
                    from PyroUbot.core.helpers.inline import BTN

                    await bot.send_message(
                        X.me.id,
                        MSG.EXP_MSG_UBOT(X),
                        reply_markup=InlineKeyboardMarkup(BTN.EXP_UBOT()),
                    )
            except Exception as e:
                print(f"[INFO] - {X.me.id} - EXPIRED CHECK: {e}")
        await asyncio.sleep(60)
