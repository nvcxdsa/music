async def notification(client, chat_id, message):
    formated_message = f"<blockquote>💌 ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ</blockquote>\n<blockquote>{message}</blockquote>"
    await client.send_message(chat_id, formated_message)