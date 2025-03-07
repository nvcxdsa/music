import asyncio

from pyrogram import Client
from pyrogram.errors import (
    ChannelsTooMuch,
    ChatAdminRequired,
    FloodWait,
    InviteRequestSent,
    UserAlreadyParticipant, ChannelPrivate,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from WinxMusic import app, Platform
from WinxMusic.core.call import Winx
from WinxMusic.core.userbot import assistants
from WinxMusic.misc import SUDOERS
from WinxMusic.utils.database import (
    get_assistant,
    get_cmode,
    get_lang,
    get_playmode,
    get_playtype,
    is_active_chat,
    is_commanddelete_on,
    is_maintenance,
    is_served_private_chat,
    set_assistant,
)
from WinxMusic.utils.inline import botplaylist_markup
from config import PLAYLIST_IMG_URL, PRIVATE_BOT_MODE
from config import SUPPORT_GROUP as SUPPORT_CHAT
from config import adminlist
from strings import get_string

links = {}


async def join_chat(message: Message, chat_id: int, _, myu: Message = None, attempts=1):
    max_attempts = len(assistants) - 1  # Set the maximum number of attempts
    userbot = await get_assistant(chat_id)

    if chat_id in links:
        invite_link = links[chat_id]
    else:
        if message.chat.username:
            invite_link = message.chat.username
            try:
                await userbot.resolve_peer(invite_link)
            except Exception:
                pass
        else:
            try:
                invite_link = await app.export_chat_invite_link(message.chat.id)
            except ChatAdminRequired:
                return await myu.edit(_["call_1"])
            except Exception as e:
                return await myu.edit(_["call_3"].format(app.mention, type(e).__name__))

        if invite_link.startswith("https://t.me/+"):
            invite_link = invite_link.replace(
                "https://t.me/+", "https://t.me/joinchat/"
            )
        links[chat_id] = invite_link

    try:
        await asyncio.sleep(1)
        await userbot.join_chat(invite_link)
    except InviteRequestSent:
        try:
            await app.approve_chat_join_request(chat_id, userbot.id)
        except Exception as e:
            return await myu.edit(_["call_3"].format(type(e).__name__))
        await asyncio.sleep(1)
        await myu.edit(_["call_6"].format(app.mention))
    except UserAlreadyParticipant:
        pass
    except ChannelsTooMuch:
        if attempts <= max_attempts:
            userbot = await set_assistant(chat_id)
            return await join_chat(message, chat_id, _, myu, attempts + 1)
        else:
            return await myu.edit(_["call_9"].format(SUPPORT_CHAT))
    except FloodWait as e:
        time = e.value
        if time < 20:
            await asyncio.sleep(time)
            return await join_chat(message, chat_id, _, myu, attempts + 1)
        else:
            if attempts <= max_attempts:
                userbot = await set_assistant(chat_id)
                return await join_chat(message, chat_id, _, myu, attempts + 1)

            return await myu.edit(_["call_10"].format(time))
    except Exception as e:
        return await myu.edit(_["call_3"].format(type(e).__name__))

    try:
        await myu.delete()
    except Exception:
        pass


def play_wrapper(command: callable):
    async def wrapper(client: Client, message: Message):
        language = await get_lang(message.chat.id)
        _ = get_string(language)
        if message.sender_chat:
            upl = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Como resolver isso?",
                            callback_data="AnonymousAdmin",
                        ),
                    ]
                ]
            )
            return await message.reply_text(_["general_4"], reply_markup=upl)

        if await is_maintenance() is False:
            if message.from_user.id not in SUDOERS:
                return

        if PRIVATE_BOT_MODE == str(True):
            if not await is_served_private_chat(message.chat.id):
                await message.reply_text(
                    "**BOT DE MÚSICA PRIVADO**\n\nSomente para chats autorizados pelo dono. Peça ao meu dono para permitir o seu chat primeiro."
                )
                return await app.leave_chat(message.chat.id)
        if await is_commanddelete_on(message.chat.id):
            try:
                await message.delete()
            except Exception:
                pass

        audio_telegram = (
            (message.reply_to_message.audio or message.reply_to_message.voice)
            if message.reply_to_message
            else None
        )
        video_telegram = (
            (message.reply_to_message.video or message.reply_to_message.document)
            if message.reply_to_message
            else None
        )
        url = await Platform.youtube.url(message)
        if audio_telegram is None and video_telegram is None and url is None:
            if len(message.command) < 2:
                if "stream" in message.command:
                    return await message.reply_text(_["str_1"])
                buttons = botplaylist_markup(_)
                return await message.reply_photo(
                    photo=PLAYLIST_IMG_URL,
                    caption=_["playlist_1"],
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
        if message.command[0][0] == "c":
            chat_id = await get_cmode(message.chat.id)
            if chat_id is None:
                return await message.reply_text(_["setting_12"])
            try:
                chat = await app.get_chat(chat_id)
            except Exception:
                return await message.reply_text(_["cplay_4"])
            channel = chat.title
        else:
            chat_id = message.chat.id
            channel = None
        try:
            is_call_active = (await app.get_chat(chat_id)).is_call_active
            if not is_call_active:
                return await message.reply_text(
                    "**Nenhum chat de vídeo ativo encontrado**\n\nPor favor, certifique-se de que você iniciou o chat de voz."
                )
        except Exception:
            pass

        playmode = await get_playmode(message.chat.id)
        playty = await get_playtype(message.chat.id)
        if playty != "Everyone":
            if message.from_user.id not in SUDOERS:
                admins = adminlist.get(message.chat.id)
                if not admins:
                    return await message.reply_text(_["admin_18"])
                else:
                    if message.from_user.id not in admins:
                        return await message.reply_text(_["play_4"])
        if message.command[0][0] == "v":
            video = True
        else:
            if "-v" in message.text:
                video = True
            else:
                video = True if message.command[0][1] == "v" else None
        if message.command[0][-1] == "e":
            if not await is_active_chat(chat_id):
                return await message.reply_text(_["play_18"])
            fplay = True
        else:
            fplay = None

            if await is_active_chat(chat_id):
                userbot = await get_assistant(message.chat.id)
                # Getting all members id that in voicechat
                try:
                    call_participants_id = [
                        member.chat.id
                        async for member in userbot.get_call_members(chat_id)
                        if member.chat
                    ]
                    # Checking if assistant id not in list so clear queues and remove active voice chat and process
                    if not call_participants_id or userbot.id not in call_participants_id:
                        await Winx.stop_stream(chat_id)
                except ChannelPrivate:
                    pass

        return await command(
            client,
            message,
            _,
            chat_id,
            video,
            channel,
            playmode,
            url,
            fplay,
        )

    return wrapper
