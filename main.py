import os
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers.start import router as start_router
from handlers.group import router as group_router
from handlers.notification import router as notify_router
from handlers.notificationboard import router as notif_board_router

from storage.notifications import create_notifications_table
from storage.user_group import create_usergroup_table
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()

async def main():

    scheduler = AsyncIOScheduler()
    scheduler.start()

    TOKEN = os.getenv('TOKEN')
    bot = Bot(TOKEN)
    dp = Dispatcher()

    dp["scheduler"] = scheduler
    dp.include_router(start_router)
    dp.include_router(group_router)
    dp.include_router(notify_router)
    dp.include_router(notif_board_router)
    


    await dp.start_polling(bot)

if __name__ == "__main__":
    create_notifications_table()
    create_usergroup_table()
    asyncio.run(main())