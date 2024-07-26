import time
import logging
import pyrogram

from pyrogram import Client
from pyrogram.errors import BadRequest
from pyrogram.raw.all import layer

from PornHub import __version__, __version_code__
from PornHub.config import API_HASH, API_ID, TOKEN, log_chat

logger = logging.getLogger(__name__)


class PornHub(Client):
    def __init__(self):
        name = self.__class__.__name__.lower()

        super().__init__(
            name=name,
            app_version=f"PornHub v{__version__}",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=TOKEN,
            plugins=dict(root="PornHub.plugins"),
            in_memory=True,
            skip_updates=False,
        )

    async def start(self):
        await super().start()

        self.start_time = time.time()

        logger.info(
            "PornHub running with Pyrogram v%s (Layer %s) started on %s. Hello!",
            pyrogram.__version__,
            layer,
            self.me.username,
        )

        start_message = (
            "<b>PornHub started!</b>\n\n"
            f"<b>Version:</b> <code>v{__version__} ({__version_code__})</code>\n"
            f"<b>Pyrogram:</b> <code>v{pyrogram.__version__}</code>"
        )

        try:
            await self.send_message(chat_id=log_chat, text=start_message)
        except BadRequest:
            logger.warning("Unable to send message to log_chat!")

    async def stop(self):
        await super().stop()
        logger.warning("PornHub stopped, Bye!")
