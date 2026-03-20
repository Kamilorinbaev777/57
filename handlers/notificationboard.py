from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, Message

from services.user_groups_service import get_user_group
from services.notificationlist import get_notification_byID, remove_notification, update_status, get_notifications
from keyboards.notificationlist import notif_kbds, notif_page_kbds, notif_page_kbds1
from keyboards.start import back_to_mainkb

from scheduler import scheduler

router = Router()

@router.callback_query(F.data == 'user_notif_list')
async def get_notification_list(
    callback: CallbackQuery
    ):
    user_id = callback.from_user.id
    await callback.message.edit_text(
        """📋 Your previous notifications\n\nReview or manage them below 👇""",
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
        print(notification)
        group_id = notification['group_id']
        group = get_user_group(user_id, group_id)
        group_title = group['title']

        run_time_from_db = notification['run_time']
        status = notification['status']
        content_type = notification['content_type']
        text = notification.get('content')
        photo = notification.get('content')
        caption = notification.get('caption')
    
    status_map = {
        "pending": "⏳ Pending",
        "success": "✅ Sent",
        "failed": "❌ Failed",
        "rejected": "Rejected"
        }
    try:
        if content_type == "photo":
            await callback.message.answer_photo(
                photo=photo,
                caption=f"📝 Your notification\n\n"
                    f"{caption}\n\n"
                    f"📅 Time: {run_time_from_db}\n"
                    f"📊 Status: {status_map.get(status, status)}\n"
                    f"👥 Group: {group_title}\n"
                    f"🆔 ID: {group_id}",
                    reply_markup=notif_page_kbds1(user_id=user_id, notif_id=notif_id)
                )
        elif content_type == "text":
            await callback.message.edit_text(
                f"📝 Your notification\n\n"
                f"{text}\n\n"
                f"📅 Time: {run_time_from_db}\n"
                f"📊 Status: {status_map.get(status, status)}\n"
                f"👥 Group: {group_title}\n"
                f"🆔 ID: {group_id}",
                reply_markup=notif_page_kbds(user_id=user_id, notif_id=notif_id)
                )
    except Exception as e:
        print(e)
        await callback.answer(
            """⚠️ Invalid notification\n\nPlease check the details and try again 👇""", 
            show_alert=True)

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
        await callback.answer(
            """⚠️ Invalid notification\n\nPlease check the details and try again 👇""", 
            show_alert=True)
    job_id = str(notification.get('job_id'))
    try:
        scheduler.remove_job(job_id)
        await callback.answer(
            """❌ Notification rejected\n\nIt has been removed and won’t be sent""",
            show_alert=True
            )
        update_status(user_id, notif_id, "rejected")
    except Exception as e:
        print(e)
        await callback.answer(
            """❌ Failed to reject the notification\n\nPlease try again 👇""", show_alert=True
            )
        
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith('del_'))
async def handle_notif_deletion(
    callback: CallbackQuery
    ):
    datas = callback.data.split('_')
    user_id = int(datas[1])
    notif_id = int(datas[2])
    notification = get_notification_byID(user_id, notif_id)
    if notification:
        status = notification.get('status')
    print(user_id, notif_id)
    try:
        if status != "pending":
            remove_notification(user_id=user_id, Notif_id=notif_id)
            await callback.message.answer(
                "🗑️ Notification deleted successfully",
                reply_markup=back_to_mainkb
                )
        else:
            await callback.answer(
                "⚠️ Please reject the notification first\n\nAfter that, you can remove it 👇",
                show_alert=True
                )
    except:
        await callback.answer(
            "❌ Failed to remove the notification",
            show_alert=True
            )

@router.callback_query(F.data == 'delete_allnotifs')
async def delete_all_notifs(
    callback: CallbackQuery
    ):
    user_id = callback.from_user.id
    notifications = get_notifications(user_id)
    try:
        for notification in notifications:
            notif_id = notification[0]
            remove_notification(user_id, notif_id)
    except:
        pass
    await callback.message.edit_text(
        "🗑️ All previous notifications deleted\n\nNothing left to worry about 👍",
        reply_markup=back_to_mainkb
        )
    await callback.answer()