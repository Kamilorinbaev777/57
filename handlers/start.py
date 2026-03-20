from aiogram import Bot, F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from keyboards.start import main_kb
router = Router()

router.message.filter(F.chat.type == "private")

@router.message(CommandStart())
async def handle_start(
    message: Message,
    bot: Bot
    ):
    bot_info = await bot.get_me()
    username = message.from_user.username
    await message.answer(
        f"""
        👋 Welcome, @{username}!\n\nLet’s set up your next notification 🔔""",
        reply_markup=main_kb(bot_info.username)
        )