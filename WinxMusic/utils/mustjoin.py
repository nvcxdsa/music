from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden
from WinxMusic import (
    LOGGER
)
from config import MUST_JOIN

async def must_join(client, message):
    try:
        if not MUST_JOIN: 
            return True
        try:
            username = MUST_JOIN
            if username.startswith("@"):
                username = username[1:]
            if username.startswith("-100"):
                user_id = int(username)
            else:
                user_id = (await client.get_chat(username)).id
            try:
                await client.get_chat_member(user_id, message.from_user.id)
                return True
            except UserNotParticipant:
                if message.chat.type in ["group", "supergroup"]:
                    chat_name = (await client.get_chat(user_id)).title
                    buttons = [
                        [
                            InlineKeyboardButton(
                                f"Join {chat_name}",
                                url=f"https://t.me/{username}"
                            )
                        ]
                    ]
                    try:
                        await client.send_message(
                            chat_id=message.chat.id,
                            text=f"❗ **You must join @{username} to use this bot!**\n\nPlease join the group and try again.",
                            reply_markup=InlineKeyboardMarkup(buttons),
                            disable_web_page_preview=True
                        )
                    except Exception as e:
                        LOGGER(__name__).error(f"Failed to send join message: {e}")
                return False
        except (ChatAdminRequired, ChatWriteForbidden):
            LOGGER(__name__).error(
                f"Make sure the bot is an admin in the chat: @{MUST_JOIN}"
            )
    except Exception as e:
        LOGGER(__name__).error(f"Error in must_join_channel: {e}")
        return True