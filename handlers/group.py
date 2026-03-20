from aiogram.types import ChatMemberUpdated
from aiogram import Router, Bot

from services.user_groups_service import add_user_group
router = Router()

@router.my_chat_member()
async def bot_added(
    event: ChatMemberUpdated,
    bot: Bot
    ):
    if event.new_chat_member.status in ("member", "administrator"):
        group_id = event.chat.id
        group_title = event.chat.title
        user_id = event.from_user.id
        if group_id and group_title:
            add_user_group(user_id, group_id, group_title)