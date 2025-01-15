from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync



# noinspection PyUnresolvedReferences

@receiver(post_save, sender=Notification)
def notify_user(sender, instance, created, **kwargs):
    
    """Automatically sends a real-time notification when a new Notification object is created."""
    if created and instance.notification_type == "real-time":
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{instance.user.id}",
            {
                'type': 'send_notification',
                'message': instance.message,
            }
        )
