from loader import *
import asyncio, handlers, middlewares, utils
from utils.notify_admins import *
from utils.set_bot_commands import set_default_commands

async def main():
    dp.startup.register(on_startup_notify)
    dp.shutdown.register(on_shutdown_notify)
    await set_default_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
