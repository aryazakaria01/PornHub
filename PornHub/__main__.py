import sys
import logging
import platform

from .bot import PornHub
from pyrogram import idle
from asyncio import get_event_loop_policy


logging.basicConfig(
    level=logging.INFO,
    format="%(name)s.%(funcName)s | %(levelname)s | %(message)s",
    datefmt="[%X]",
)
logging.getLogger("pyrogram.syncer").setLevel(logging.WARNING)
logging.getLogger("pyrogram.client").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def main():
    pornhub = PornHub()

    try:
        await pornhub.start()

        if "test" not in sys.argv:
            await idle()
    except KeyboardInterrupt:
        logger.warning("Forced stop, Bye!")
    finally:
        await pornhub.stop()


if __name__ == "__main__":
    get_event_loop_policy().get_event_loop().run_until_complete(main())
