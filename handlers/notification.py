from aiogram import Bot, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states import notification
from states.notification import newNotificaton
from keyboards.start import main_kb, group_list, cancel_notifykb, back_to_mainkb
from services.notificationlist import add_notification, get_notification_bytime, update_status, update_job_id
from scheduler import scheduler
from datetime import datetime
router = Router()

router.message.filter(F.chat.type == "private")

async def send_scheduled_message(bot, group_id, text, notif_id, user_id):
    try:        
        update_status(user_id, notif_id, "success")
        await bot.send_message(group_id, text)
    except: 
        update_status(user_id, notif_id, "failed")

async def send_scheduled_photo(bot, group_id, photo, caption, notif_id, user_id):
    try:
        update_status(user_id, notif_id, "success")
        await bot.send_photo(group_id, photo, caption)
    except:
        update_status(user_id, notif_id, "failed")

@router.callback_query(F.data == 'notify_bday')
async def handle_group_buttons(
    callback: CallbackQuery,
    state: FSMContext
    ):
    user_id = callback.from_user.id
    await state.set_state(newNotificaton.group)
    await callback.message.edit_text(
        "Choose a group from the list",
        reply_markup=group_list(user_id=user_id)
        )
    await callback.answer()

@router.callback_query(F.data == 'backto_main')
async def back_to_main(
    callback: CallbackQuery,
    bot: Bot,
    state: FSMContext
    ):
    await state.clear()
    bot_info = await bot.get_me()
    username = callback.from_user.username
    await callback.message.edit_text(
        f"Welcome @{username}",
        reply_markup=main_kb(bot_info.username)
        )
    await callback.answer()

@router.callback_query(F.data == 'cancel_notify')
async def cancel_notification(
    callback: CallbackQuery,
    state: FSMContext
    ):
    await callback.answer()

    await state.clear()

    try:
        if callback.message:
            await callback.message.edit_text(
                "Notification cancelled",
                reply_markup=back_to_mainkb
            )
    except:
        await callback.message.edit_text(
            "Notification cancelled",
            reply_markup=back_to_mainkb
        )

@router.callback_query(lambda c: c.data.startswith("to_"))
async def handle_group_button(
    callback: CallbackQuery,
    state: FSMContext
    ):
    group_id = int(callback.data.split('_')[1])
    await state.update_data(group=group_id)
    await state.set_state(newNotificaton.content)
    await callback.message.edit_text(
        "Send me your notification message",
        reply_markup=cancel_notifykb
        )
    await callback.answer()

@router.message(newNotificaton.content)
async def handle_notification_send(
    message: Message,
    state: FSMContext,
    bot: Bot
    ):
    if message.photo:
        await state.update_data(
            content_type="photo",
            content=message.photo[-1].file_id,
            caption=message.caption
            )
    elif message.text:
        await state.update_data(
            content_type="text",
            content=message.text
            )
    await state.set_state(newNotificaton.date)
    await message.answer("Send me exact date time in the format YYYY-MM-DD HH:MM")

@router.message(newNotificaton.date)
async def handle_date_state(
    message: Message,
    state: FSMContext,
    bot: Bot
    ):
    try: 
        date = message.text
        run_time = datetime.strptime(date, "%Y-%m-%d %H:%M")
        print("Scheduler running:", scheduler.running)
        print("Now:", datetime.now())
        print("Run time:", run_time)
    except Exception:
        await message.answer(
            "Invalid data!, try again",
            reply_markup=back_to_mainkb
            )
        return

    user_id = message.from_user.id
    data = await state.get_data()
    group_id = data["group"]
    content_type = data["content_type"]
    content = data["content"]
    caption = data.get("caption")
    status = "pending"

    notification = get_notification_bytime(user_id, run_time)
    notif_id = add_notification(
        user_id,
        group_id,
        content_type,
        content,
        caption,
        run_time,
        status,
        13
        )
    await state.clear()
    try:
        if content_type == "photo":
            job = scheduler.add_job(
                send_scheduled_photo,
                "date",
                run_date=run_time,
                args=[message.bot, group_id, content, caption, notif_id, user_id]
            )
        elif content_type == "text":
            job = scheduler.add_job(
                send_scheduled_message,
                "date",
                run_date=run_time,
                args=[message.bot, group_id, content, notif_id, user_id]
            )
            
        job_id = job.id
        update_job_id(user_id, notif_id, job_id)
        
        await message.answer(
            "Notification has been scheduled successfully!",
            reply_markup=back_to_mainkb
            )
        print("MAIN scheduler:", id(scheduler))
    except Exception:
        await message.answer("Notification was not scheduled",
                             reply_markup=back_to_mainkb)