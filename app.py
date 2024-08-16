from aiogram import Dispatcher
from loader import *
import middlewares, filters, handlers, asyncio
from utils.notify_admins import *
from utils.set_bot_commands import set_default_commands
from piston import Interpreter
import middlewares, filters, handlers, asyncio

async def main():
    interpreter = Interpreter()
    dp.startup.register(on_startup_notify)
    dp.shutdown.register(on_shutdown_notify)
    try:db.create_table_users()
    except Exception as err:print(err)
    try:ans.create_table_user_answers()
    except Exception as err:print(err)
    await set_default_commands(bot)
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    asyncio.run(main())