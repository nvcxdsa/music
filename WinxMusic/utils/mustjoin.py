from pyrogram.errors import UserNotParticipant, ChatAdminRequired, FloodWait
import asyncio
import time

async def check_user_membership(self, user_id, group_id):
        result = {
            "is_member": False,
            "status": None,
            "details": None,
            "raw_status": None
        }
        
        # Add a small delay to avoid rate limits
        await asyncio.sleep(0.5)
        
        try:
            # Normalize group_id if it's a numeric string with -100 prefix
            if isinstance(group_id, str) and group_id.startswith("-100") and group_id[4:].isdigit():
                group_id = int(group_id)
            
            # Get chat member information
            member = await self.client.get_chat_member(group_id, user_id)
            
            # Store the raw status for detailed debugging
            result["raw_status"] = member.status
            
            # Check member status - including restricted as a valid membership status
            if member.status in ["member", "administrator", "creator", "restricted"]:
                result["is_member"] = True
                result["status"] = member.status
                result["details"] = f"User is a member of the group with status: {member.status}"
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
            # Wait the required time before retrying
            await asyncio.sleep(e.x)
            # Recursively retry the check after waiting
            return await self.check_user_membership(user_id, group_id)
            
        except Exception as e:
            result["status"] = "error"
            result["details"] = str(e)
        
        return result["is_member"], result