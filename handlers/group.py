from aiogram.types import ChatMemberUpdated
from aiogram import Router, Bot

from services.user_groups_service import add_user_group, delete_user_group
router = Router()

@router.my_chat_member()
async def bot_added(
    event: ChatMemberUpdated,
    bot: Bot
    ):
    group_id = event.chat.id
    user_id = event.from_user.id

    old_status = event.old_chat_member.status
    new_status = event.new_chat_member.status

    if new_status in ["left", "kicked"]:
        print("Bot removed from group:", group_id)

        delete_user_group(user_id, group_id)
    
    if new_status in ("member", "administrator"):
        group_title = event.chat.title
        
        if group_id and group_title:
            add_user_group(user_id, group_id, group_title)