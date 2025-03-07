import asyncio
import speedtest
from pyrogram import filters
from WinxMusic import app
from WinxMusic.misc import SUDOERS
from strings import get_command

SPEEDTEST_COMMAND = get_command("SPEEDTEST_COMMAND")


def testspeed(m):
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = m.edit("⇆ Menguji **download** ... ⬇️")
        test.download()
        m = m.edit("⇆ Menguji **upload** ... ⬆️")
        test.upload()
        test.results.share()
        result = test.results.dict()
        m = m.edit("↻ Membagikan hasil SpeedTest ... 📊")
    except Exception as e:
        return m.edit(f"⚠️ Kesalahan: {e}")
    return result


@app.on_message(filters.command(SPEEDTEST_COMMAND) & SUDOERS)
async def speedtest_function(client, message):
    m = await message.reply_text("🚀 **Memulai SpeedTest**...")
    loop = asyncio.get_event_loop_policy().get_event_loop()
    result = await loop.run_in_executor(None, testspeed, m)
    output = f"""**Hasil SpeedTest** 📊

<u>**Klien:**</u>
🌐 **ISP :** {result['client']['isp']}
🏳️ **Negara :** {result['client']['country']}

<u>**Server:**</u>
🌍 **Nama :** {result['server']['name']}
🇦🇺 **Negara:** {result['server']['country']}, {result['server']['cc']}
💼 **Sponsor:** {result['server']['sponsor']}
⚡ **Latensi:** {result['server']['latency']} ms  
🏓 **Ping :** {result['ping']} ms"""
    msg = await app.send_photo(
        chat_id=message.chat.id, photo=result["share"], caption=output
    )
    await m.delete()
