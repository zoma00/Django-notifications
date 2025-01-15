# Django Notifications App

This project demonstrates how to implement a robust notifications system in Django, including real-time notifications using WebSockets with Django Channels and Redis.

## Features

- **Real-Time Notifications**: Delivered instantly using WebSockets.
- **Batch Notifications**: Scheduled and grouped notifications.
- **Email Notifications**: Sent to users via email channels.
- **Notification Types**: Support for multiple notification types (e.g., real-time, batch, email).
- **Asynchronous Processing**: Decoupled notification logic with Celery and Redis.
- **REST API Integration**: API endpoints to create, fetch, and update notifications.
- **Caching**: Enhanced performance through Django's caching framework.
- **Monitoring and Testing**: Robust error monitoring with Sentry and comprehensive unit tests.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Database Model](#database-model)
5. [Real-Time Notifications](#real-time-notifications)
6. [Batch Notifications](#batch-notifications)
7. [API Endpoints](#api-endpoints)
8. [Testing and Monitoring](#testing-and-monitoring)
9. [License](#license)

---

## Prerequisites

- Python 3.x
- Django 4.x
- Django REST Framework
- Django Channels
- Redis
- Celery
- WebSockets-compatible front end

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/Django-notifications.git
   cd django-notifications
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Redis for WebSockets and Celery:
   ```bash
   redis-server
   ```

4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

---

## Configuration

### Channels and WebSockets

1. Add `channels` to your `INSTALLED_APPS` in `settings.py`.
2. Configure the channel layers:
   ```python
   CHANNEL_LAYERS = {
       "default": {
           "BACKEND": "channels_redis.core.RedisChannelLayer",
           "CONFIG": {
               "hosts": [("127.0.0.1", 6379)],
           },
       },
   }
   ```

---

## Database Model

The `Notification` model stores notifications with fields for user, message, read status, and type:

```python
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} - {self.message}"
```

---

## Real-Time Notifications

Real-time notifications are sent using WebSockets. Django Channels enables WebSocket support:

- Use a WebSocket consumer to handle notification events.
- Use Redis as the message broker.

Example consumer:
```python
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("notifications", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notifications", self.channel_name)

    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event["message"]))
```

---

## Batch Notifications

Batch notifications are handled asynchronously using Celery:

1. Configure Celery in your Django project:
   ```python
   CELERY_BROKER_URL = 'redis://localhost:6379/0'
   CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
   ```

2. Example task:
   ```python
   from celery import shared_task
   from .models import Notification

   @shared_task
   def send_batch_notifications():
       # Fetch and process batch notifications
       pass
   ```

---

## API Endpoints

- **List Notifications**: Fetch all notifications for a user.
- **Create Notification**: Add a new notification.
- **Update Notification**: Mark a notification as read.

Example serializer:
```python
from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
```

---

## Testing and Monitoring

- **Testing**: Use Django's `TestCase` to write unit tests.
- **Monitoring**: Use Sentry to capture and analyze errors:
  ```bash
  pip install sentry-sdk
  ```

---

## License

This project is licensed under the MIT License.
