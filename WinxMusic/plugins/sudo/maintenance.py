from pyrogram import filters, Client
from pyrogram.types import Message

from WinxMusic import app
from WinxMusic.misc import SUDOERS
from WinxMusic.utils.database import (
    get_lang,
    is_maintenance,
    maintenance_off,
    maintenance_on,
)
from strings import get_command, get_string

MAINTENANCE_COMMAND = get_command("MAINTENANCE_COMMAND")


@app.on_message(filters.command(MAINTENANCE_COMMAND) & SUDOERS)
async def maintenance(_client: Client, message: Message):
    try:
        language = await get_lang(message.chat.id)
        _ = get_string(language)
    except Exception:
        _ = get_string("pt")
    usage = _["maint_1"]
    if len(message.command) != 2:
        return await message.reply_text(usage)
    message.chat.id
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        if await is_maintenance() is False:
            await message.reply_text(_["maint_6"])
        else:
            await maintenance_on()
            await message.reply_text(_["maint_2"])
    elif state == "disable":
        if await is_maintenance() is False:
            await maintenance_off()
            await message.reply_text(_["maint_3"])
        else:
            await message.reply_text(_["maint_5"])
    else:
        await message.reply_text(usage)
