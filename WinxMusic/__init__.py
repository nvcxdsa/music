from WinxMusic.core.bot import WinxBot
from WinxMusic.core.dir import dirr
from WinxMusic.core.git import git
from WinxMusic.core.userbot import Userbot
from WinxMusic.misc import dbb, heroku, sudo
from .core.cookies import save_cookies

from .logging import LOGGER
import config

# Bot Client
app = WinxBot(
    "FloraMusic",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    sleep_threshold=240,
    max_concurrent_transmissions=6,
    workers=50,
)

# Assistant Client
userbot = Userbot()

for i, session in enumerate(config.STRING_SESSIONS, start=1):
    userbot.add(
        f"FloraString{i}",
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        session_string=session.strip(),
    )

# Directories
dirr()

# # Check Git Updates
git()

# Initialize Memory DB
dbb()

# Heroku APP
heroku()

# Load Sudo Users from DB
sudo()

from .platforms import PlaTForms

Platform = PlaTForms()

HELPABLE = {}
