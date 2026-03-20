from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, Message

from services.user_groups_service import get_user_group
from services.notificationlist import get_notification_byID, remove_notification, update_status
from keyboards.notificationlist import notif_kbds, notif_page_kbds
from keyboards.start import back_to_mainkb
from keyboards.notificationlist import notif_page_kbds

from scheduler import scheduler

router = Router()

@router.callback_query(F.data == 'user_notif_list')
async def get_notification_list(
    callback: CallbackQuery
    ):
    user_id = callback.from_user.id
    await callback.message.edit_text(
        "Your previous notifications",
        reply_markup=notif_kbds(user_id)
        )
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith('view_'))
async def get_notif_details(
    callback: CallbackQuery
    ):
    user_id = callback.from_user.id
    notif_id = int(callback.data.split('_')[1])
    notification = get_notification_byID(user_id=user_id, Notifid=notif_id)
    
    if notification:
        #print(notification)
        group_id = notification['group_id']
        group = get_user_group(user_id, group_id)
        group_title = group['title']

        run_time = notification['run_time']
        status = notification['status']
        content_type = notification['content_type']
        text = notification.get('content')
        photo = notification.get('content')
        caption = notification.get('caption')
    
    try:
        if content_type == "photo":
            await callback.message.answer_photo(
                photo=photo,
                caption=f"{caption}\n"
                f"Details:\nDate: {run_time}"
                f"\nStatus: {status}"
                f"\nTo group: {group_title}: with id: {group_id}",
                reply_markup=back_to_mainkb
                )
        elif content_type == "text":
            await callback.message.answer(
                f"{text}\n"
                f"Details:\nDate: {run_time}"
                f"\nStatus: {status}"
                f"\nTo group: {group_title}: with id: {group_id}",
                reply_markup=notif_page_kbds(user_id=user_id, notif_id=notif_id)
                )
    except Exception:
        await callback.answer("Invalid Notification", show_alert=True)

    await callback.answer()

@router.callback_query(lambda c: c.data.startswith('reject_'))
async def reject_notif(
    callback: CallbackQuery
    ):
    print("Existing jobs:", scheduler.get_jobs())
    print("HANDLER scheduler:", id(scheduler))
    data = callback.data.split('_')
    user_id = int(data[1])
    notif_id = int(data[2])
    notification = get_notification_byID(user_id, notif_id)
    if not notification:
        await callback.answer("Invalid notification", show_alert=True)
    job_id = str(notification.get('job_id'))
    try:
        scheduler.remove_job(job_id)
        await callback.message.edit_text("Notification rejected successfully")
        update_status(user_id, notif_id, "rejected")
    except Exception as e:
        print(e)
        await callback.answer("Failed to reject", show_alert=True)
        
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith('del_'))
async def handle_notif_deletion(
    callback: CallbackQuery
    ):
    datas = callback.data.split('_')
    user_id = int(datas[1])
    notif_id = int(datas[2])
    print(user_id, notif_id)
    try:
        remove_notification(user_id=user_id, Notif_id=notif_id)
        await callback.message.edit_text(
            "Notification deleted successfully!",
            reply_markup=back_to_mainkb
            )
    except:
        await callback.answer(
            "An error occured while removing notification",
            show_alert=True
            )
        await callback.message.edit_text(
            "Failed",
            reply_markup=back_to_mainkb
            )

