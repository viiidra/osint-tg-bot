import asyncio
import json
import logging
import sys
import httpx

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from bot.configuration import bot_configuration as bot_config
from bot.utils import set_commands, on_startup, on_shutdown
from bot.handlers.commands import commands_router
from bot.handlers.messages import messages_router
from bot.handlers.admin import admin_router
from bot.middlewares.antiflood import AntiFloodMiddleware


async def identify_myself() -> str | None:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get('https://ipapi.co/json/')
            location = json.loads(response.text)
            return (f'IP: {location["ip"]}, '
                    f'Location: {location["city"]}, '
                    f'{location["region"]}, '
                    f'{location["country_name"]}')
    except:
        return 'Unknown IP'


async def main() -> None:
    logging.basicConfig(level=bot_config.logging_level,
                        format='%(asctime)s %(name)s %(levelname)s: %(funcName)s:%(lineno)d - %(message)s',
                        datefmt='%d.%m.%Y %H:%M:%S', stream=sys.stdout)
    bot = Bot(token=bot_config.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    logger = logging.getLogger(__name__)

    await set_commands(bot=bot)
    try:
        dp = Dispatcher()
        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)
        dp.message.middleware(AntiFloodMiddleware(1))
        dp.include_routers(
            admin_router,
            # messages_router,
            commands_router,
            messages_router
        )
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info(f'Starting Bot from {await identify_myself()}')
        await dp.start_polling(bot)
    except Exception(KeyboardInterrupt, SystemExit):
        logger.info('Bot stopped!')
    except Exception as _ex:
        logger.error(repr(_ex))
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as _ex:
        logging.error(f"Can't run the bot! {repr(_ex)}")
    finally:
        logging.info("Bot stopped!")
        exit(0)
