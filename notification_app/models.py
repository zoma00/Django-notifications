from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)  # Ensure this exists!
    created_at = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(max_length=50)  # e.g., 'real-time', 'batch', 'email'

    def __str__(self):
        return f"{self.user.username} - {self.message}"

    def is_real_time(self):
        """Returns True if the notification is real-time"""
        return self.notification_type == "real-time"

# Example Usage (This should be done outside the class definition)


notification = Notification(user=User.objects.first(), message="New message", notification_type="real-time")
if notification.is_real_time():
    print("This is a real-time notification!")
