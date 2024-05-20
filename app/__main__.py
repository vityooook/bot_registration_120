from loguru import logger
import asyncio

from loader import dp, bot
# * import default commands for menu /start
from services import set_default_commands
# * import all routers
from handlers import get_handlers_router


async def main():
    # Declare all routers(handlers) in dispatcher
    dp.include_router(get_handlers_router())
    await set_default_commands(dp)
    # Delete old line command
    await bot.delete_webhook(drop_pending_updates=True)
    logger.debug("Bot started!")
    # Launch bot
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
