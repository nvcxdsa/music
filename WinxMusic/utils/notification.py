from WinxMusic import app
async def notification(chat_id, message):
    formated_message = f"<blockquote>💌 ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ</blockquote>\n<blockquote>{message}</blockquote>"
    await app.send_message(chat_id, formated_message)