from celery import shared_task
from .models import Notification
from django.utils.timezone import now

@shared_task
def send_batch_notifications():
    """Sends batch notifications asynchronously."""
    notifications = Notification.objects.filter(is_read=False)
    for notification in notifications:
        print(f"Sending notification: {notification.message}")
    return f"{notifications.count()} notifications processed at {now()}"
