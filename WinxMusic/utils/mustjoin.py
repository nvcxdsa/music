from pyrogram.errors import UserNotParticipant, ChatAdminRequired, FloodWait
import asyncio
import time

async def check_user_membership(client, user_id, group_id):
    result = {
        "is_member": False,
        "status": None,
        "details": None
    }
    
    try:
        if isinstance(group_id, str) and group_id.startswith("-100") and group_id[4:].isdigit():
            group_id = int(group_id)
        member = await client.get_chat_member(group_id, user_id)
        if member.status in ["member", "administrator", "creator"]:
            result["is_member"] = True
            result["status"] = member.status
            result["details"] = "User is a member of the group"
        else:
            result["status"] = member.status
            result["details"] = f"User is in the group but with status: {member.status}"
    except UserNotParticipant:
        result["status"] = "not_participant"
        result["details"] = "User is not a member of the group"
    except ChatAdminRequired:
        result["status"] = "admin_required"
        result["details"] = "Bot needs admin privileges to check membership"
        
    except FloodWait as e:
        result["status"] = "flood_wait"
        result["details"] = f"Rate limited. Try again after {e.x} seconds"
        await asyncio.sleep(e.x)
        
    except Exception as e:
        result["status"] = "error"
        result["details"] = str(e)
    return result["is_member"], result