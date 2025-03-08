from pyrogram import Client
from pyrogram.errors import UserNotParticipant
from pyrogram.types import ChatMember

async def is_user_member(client: Client, user_id: int, group_id: int) -> bool:
    try:
        member: ChatMember = await client.get_chat_member(group_id, user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
        return False
    except UserNotParticipant:
        return False
    except Exception as e:
        print(f"Error checking membership: {e}")
        return False
