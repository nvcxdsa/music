from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from WinxMusic import app
from WinxMusic.core.call import Winx
from WinxMusic.misc import SUDOERS
from WinxMusic.plugins import extra_plugins_enabled
from WinxMusic.utils.database import (
    delete_filter,
    get_cmode,
    get_lang,
    is_active_chat,
    is_commanddelete_on,
    is_maintenance,
    is_nonadmin_chat,
    set_loop,
)
from config import BANNED_USERS, adminlist, PREFIXES
from strings import get_command, get_string

STOP_COMMAND = get_command("STOP_COMMAND")


@app.on_message(filters.command(STOP_COMMAND, PREFIXES) & filters.group & ~BANNED_USERS)
async def stop_music(cli, message: Message):
    if await is_maintenance() is False:
        if message.from_user.id not in SUDOERS:
            return
    if not len(message.command) < 2:
        if extra_plugins_enabled:
            if not message.command[0][0] == "c" and not message.command[0][0] == "e":
                filter = " ".join(message.command[1:])
                deleted = await delete_filter(message.chat.id, filter)
                if deleted:
                    return await message.reply_text(f"**ᴅᴇʟᴇᴛᴇᴅ ғɪʟᴛᴇʀ {filter}.**")
                else:
                    return await message.reply_text("**ɴᴏ sᴜᴄʜ ғɪʟᴛᴇʀ.**")

    if await is_commanddelete_on(message.chat.id):
        try:
            await message.delete()
        except Exception:
            pass
    try:
        language = await get_lang(message.chat.id)
        _ = get_string(language)
    except Exception:
        _ = get_string("pt")

    if message.sender_chat:
        upl = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="How to Fix this? ",
                        callback_data="AnonymousAdmin",
                    ),
                ]
            ]
        )
        return await message.reply_text(_["general_4"], reply_markup=upl)

    if message.command[0][0] == "c":
        chat_id = await get_cmode(message.chat.id)
        if chat_id is None:
            return await message.reply_text(_["setting_12"])
        try:
            await app.get_chat(chat_id)
        except Exception:
            return await message.reply_text(_["cplay_4"])
    else:
        chat_id = message.chat.id
    if not await is_active_chat(chat_id):
        return await message.reply_text(_["general_6"])
    is_non_admin = await is_nonadmin_chat(message.chat.id)
    if not is_non_admin:
        if message.from_user.id not in SUDOERS:
            admins = adminlist.get(message.chat.id)
            if not admins:
                return await message.reply_text(_["admin_18"])
            else:
                if message.from_user.id not in admins:
                    return await message.reply_text(_["admin_19"])
    try:
        check = db.get(chat_id)
        if check[0].get("mystic"):
            await check[0].get("mystic").delete()
    except Exception:
        pass
    await Winx.stop_stream(chat_id)
    await set_loop(chat_id, 0)
    await message.reply_text(_["admin_9"].format(message.from_user.mention))
