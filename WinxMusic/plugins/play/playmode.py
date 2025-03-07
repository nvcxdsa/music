from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, Message

from WinxMusic import app
from WinxMusic.utils.database import get_playmode, get_playtype, is_nonadmin_chat
from WinxMusic.utils.decorators import language
from WinxMusic.utils.inline.settings import playmode_users_markup
from config import BANNED_USERS, PREFIXES
from strings import get_command

PLAYMODE_COMMAND = get_command("PLAYMODE_COMMAND")


@app.on_message(filters.command(PLAYMODE_COMMAND, PREFIXES) & filters.group & ~BANNED_USERS)
@language
async def playmode_(_client: Client, message: Message, _):
    playmode = await get_playmode(message.chat.id)
    if playmode == "Direct":
        Direct = True
    else:
        Direct = None
    is_non_admin = await is_nonadmin_chat(message.chat.id)
    if not is_non_admin:
        Group = True
    else:
        Group = None
    playty = await get_playtype(message.chat.id)
    if playty == "Everyone":
        Playtype = None
    else:
        Playtype = True
    buttons = playmode_users_markup(_, Direct, Group, Playtype)
    response = await message.reply_text(
        _["playmode_1"].format(message.chat.title),
        reply_markup=InlineKeyboardMarkup(buttons),
    )
