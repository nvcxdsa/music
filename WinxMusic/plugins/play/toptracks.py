import asyncio

from pyrogram import filters, Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import ChatAdminRequired, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, CallbackQuery

from WinxMusic import app
from WinxMusic.utils.database import (
    get_assistant,
    get_global_tops,
    get_particulars,
    get_userss,
)
from WinxMusic.utils.decorators import language_cb
from WinxMusic.utils.decorators.play import join_chat
from WinxMusic.utils.inline.playlist import (
    botplaylist_markup,
    failed_top_markup,
    top_play_markup,
)
from WinxMusic.utils.stream.stream import stream
from config import BANNED_USERS

loop = asyncio.get_running_loop()


@app.on_callback_query(filters.regex("get_playmarkup") & ~BANNED_USERS)
@language_cb
async def get_play_markup(_client: Client, callback_query: CallbackQuery, _):
    try:
        await callback_query.answer()
    except Exception:
        pass
    buttons = botplaylist_markup(_)
    return await callback_query.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex("get_top_playlists") & ~BANNED_USERS)
@language_cb
async def get_topz_playlists(_client: Client, callback_query: CallbackQuery, _):
    try:
        await callback_query.answer()
    except Exception:
        pass
    buttons = top_play_markup(_)
    return await callback_query.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex("SERVERTOP") & ~BANNED_USERS)
@language_cb
async def server_to_play(_client: Client, callback_query: CallbackQuery, _):
    message = callback_query.message
    userbot = await get_assistant(callback_query.message.chat.id)
    try:
        try:
            get = await app.get_chat_member(callback_query.message.chat.id, userbot.id)
        except ChatAdminRequired:
            return await myu.edit(
                _["call_1"],
                show_alert=True,
            )
        if get.status == ChatMemberStatus.BANNED:
            try:
                await app.unban_chat_member(chat_id, userbot.id)
            except Exception:
                return await myu.edit(
                    text=_["call_2"].format(userbot.username, userbot.id),
                )
    except UserNotParticipant:
        myu = await message.reply_text("❣️")
        await join_chat(message, message.chat.id, _, myu)

    chat_id = callback_query.message.chat.id
    user_name = callback_query.from_user.first_name
    try:
        await callback_query.answer()
    except Exception:
        pass
    callback_data = callback_query.data.strip()
    what = callback_data.split(None, 1)[1]
    mystic = await callback_query.edit_message_text(
        _["tracks_1"].format(
            what,
            callback_query.from_user.first_name,
        )
    )
    upl = failed_top_markup(_)
    if what == "Global":
        stats = await get_global_tops()
    elif what == "Group":
        stats = await get_particulars(chat_id)
    elif what == "Personal":
        stats = await get_userss(callback_query.from_user.id)
    if not stats:
        return await mystic.edit(_["tracks_2"].format(what), reply_markup=upl)

    def get_stats():
        results = {}
        for i in stats:
            top_list = stats[i]["spot"]
            results[str(i)] = top_list
            list_arranged = dict(
                sorted(
                    results.items(),
                    key=lambda item: item[1],
                    reverse=True,
                )
            )
        if not results:
            return mystic.edit(_["tracks_2"].format(what), reply_markup=upl)
        details = []
        limit = 0
        for vidid, count in list_arranged.items():
            if vidid == "telegram":
                continue
            if limit == 10:
                break
            limit += 1
            details.append(vidid)
        if not details:
            return mystic.edit(_["tracks_2"].format(what), reply_markup=upl)
        return details

    try:
        details = await loop.run_in_executor(None, get_stats)
    except Exception as e:
        print(e)
        return
    try:
        await stream(
            _,
            mystic,
            callback_query.from_user.id,
            details,
            chat_id,
            user_name,
            callback_query.message.chat.id,
            video=False,
            streamtype="playlist",
        )
    except Exception as e:
        ex_type = type(e).__name__
        err = e if ex_type == "AssistantErr" else _["general_3"].format(ex_type)
        return await mystic.edit_text(err)
    return await mystic.delete()
