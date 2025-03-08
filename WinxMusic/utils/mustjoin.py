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
            try:
                await client.get_chat_member(user_id, message.from_user.id)
                return True
            except UserNotParticipant:
                return False
        except (ChatAdminRequired, ChatWriteForbidden):
            LOGGER(__name__).error(
                f"Make sure the bot is an admin in the chat: @{MUST_JOIN}"
            )
    except Exception as e:
        LOGGER(__name__).error(f"Error in must_join_channel: {e}")
        return True