from pyrogram import filters, Client
from pyrogram.types import Message

from WinxMusic import app
from WinxMusic.misc import SUDOERS
from WinxMusic.utils.database import add_gban_user, remove_gban_user
from WinxMusic.utils.decorators.language import language
from config import BANNED_USERS
from strings import command, get_command

BLOCK_COMMAND = get_command("BLOCK_COMMAND")
UNBLOCK_COMMAND = get_command("UNBLOCK_COMMAND")
BLOCKED_COMMAND = get_command("BLOCKED_COMMAND")


@app.on_message(filters.command(BLOCK_COMMAND) & SUDOERS)
@language
async def useradd(_client: Client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if user.id in BANNED_USERS:
            return await message.reply_text(_["block_1"].format(user.mention))
        await add_gban_user(user.id)
        BANNED_USERS.add(user.id)
        await message.reply_text(_["block_2"].format(user.mention))
        return
    if message.reply_to_message.from_user.id in BANNED_USERS:
        return await message.reply_text(
            _["block_1"].format(message.reply_to_message.from_user.mention)
        )
    await add_gban_user(message.reply_to_message.from_user.id)
    BANNED_USERS.add(message.reply_to_message.from_user.id)
    await message.reply_text(
        _["block_2"].format(message.reply_to_message.from_user.mention)
    )


@app.on_message(filters.command(UNBLOCK_COMMAND) & SUDOERS)
@language
async def userdel(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if user.id not in BANNED_USERS:
            return await message.reply_text(_["block_3"])
        await remove_gban_user(user.id)
        BANNED_USERS.remove(user.id)
        await message.reply_text(_["block_4"])
        return
    user_id = message.reply_to_message.from_user.id
    if user_id not in BANNED_USERS:
        return await message.reply_text(_["block_3"])
    await remove_gban_user(user_id)
    BANNED_USERS.remove(user_id)
    await message.reply_text(_["block_4"])


@app.on_message(filters.command(BLOCKED_COMMAND) & SUDOERS)
@language
async def sudoers_list(client, message: Message, _):
    if not BANNED_USERS:
        return await message.reply_text(_["block_5"])
    mystic = await message.reply_text(_["block_6"])
    msg = _["block_7"]
    count = 0
    for users in BANNED_USERS:
        try:
            user = await app.get_users(users)
            user = user.first_name if not user.mention else user.mention
            count += 1
        except Exception:
            continue
        msg += f"{count}➤ {user}\n"
    if count == 0:
        return await mystic.edit_text(_["block_5"])
    else:
        return await mystic.edit_text(msg)


__MODULE__ = "Blacklist"
__HELP__ = f"""
🤖 {command("BLACKLISTCHAT_COMMAND")} [ID obrolan] - Blokir obrolan mana pun agar tidak menggunakan Bot Musik.
🤖 {command("WHITELISTCHAT_COMMAND")} [ID obrolan] - Membuka blokir obrolan dari daftar blokir agar dapat menggunakan Bot Musik.
🤖 {command("BLACKLISTEDCHAT_COMMAND")} - Periksa semua obrolan yang diblokir.
🤖 {command("BLOCK_COMMAND")} [Nama pengguna atau balas ke pengguna] - Mencegah pengguna menggunakan perintah bot.
🤖 {command("UNBLOCK_COMMAND")} [Nama pengguna atau balas ke pengguna] - Menghapus pengguna dari daftar blokir bot.
🤖 {command("BLOCKED_COMMAND")} - Periksa daftar pengguna yang diblokir.
🤖 {command("GBAN_COMMAND")} [Nama pengguna atau balas ke pengguna] - Melarang pengguna dari semua obrolan yang dilayani dan mencegah mereka menggunakan bot Anda.
🤖 {command("UNGBAN_COMMAND")} [Nama pengguna atau balas ke pengguna] - Menghapus pengguna dari daftar larangan global dan mengizinkan mereka menggunakan bot Anda.
🤖 {command("GBANNED_COMMAND")} - Periksa daftar pengguna yang dilarang secara global.
"""
