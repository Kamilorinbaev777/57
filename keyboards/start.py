from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from services.user_groups_service import get_user_group, get_users_groups

def main_kb(bot_username: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="Add to group",
                url=f"https://t.me/{bot_username}?startgroup=true",
                style='primary'
                )],
            [InlineKeyboardButton(
                text="Schedule",
                callback_data='notify_bday',
                style='success'
                )],
            [InlineKeyboardButton(
                text="My notifications",
                callback_data='user_notif_list'
                )]
            ]
        )

def group_list(user_id):
    keyboard = []
    groups = get_users_groups(user_id=user_id)

    for group in groups:
        user_id, group_id, title = group

        keyboard.append(
            [InlineKeyboardButton(
                text=f"to {title}",
                callback_data=f"to_{group_id}"
                )]
            )

    keyboard.append(
        [InlineKeyboardButton(
            text="Back",
            callback_data='backto_main'
            )]
        )
    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
        )

cancel_notifykb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text="Cancel",
            callback_data='cancel_notify',
            style='danger'
            )]
        ]
    )

back_to_mainkb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text="Back",
            callback_data='backto_main'
            )]
        ]
    )