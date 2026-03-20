from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from services.notificationlist import get_notifications
def notif_kbds(user_id):
    keyboard = []

    notifs = get_notifications(user_id=user_id)
    for notif in notifs:
        try:    
            notif_id = notif[0] #notification id
            title = notif[6] #date of event

            keyboard.append([
                InlineKeyboardButton(
                    text=title,
                    callback_data=f"view_{notif_id}"
                    )
                ])
        except Exception:
            pass

    if len(keyboard) > 2:
        keyboard.append(
            [InlineKeyboardButton(
                text="Delete all",
                callback_data='delete_allnotifs',
                style='danger'
                )]
            )

    keyboard.append(
        [InlineKeyboardButton(
            text="Back",
            callback_data='backto_main'
            )]
        )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def notif_page_kbds(user_id, notif_id):    
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="Reject",
                callback_data=f'reject_{user_id}_{notif_id}',
                style='danger'
                )],
            [InlineKeyboardButton(
                text="Delete",
                callback_data=f'del_{user_id}_{notif_id}',
                style='danger'
                )],
            [InlineKeyboardButton(
                text="Back",
                callback_data='backto_main'
                )],
        ]
    )

def notif_page_kbds1(user_id, notif_id):    
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="Reject",
                callback_data=f'reject_{user_id}_{notif_id}',
                style='danger'
                )],
            [InlineKeyboardButton(
                text="Delete",
                callback_data=f'del_{user_id}_{notif_id}',
                style='danger'
                )]
        ]
    )