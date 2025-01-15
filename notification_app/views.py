from django.contrib.auth.models import User
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from faker import Faker
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from django.shortcuts import render

def notifications_page(request):
    return render(request, 'notification_app/notifications.html')
class NotificationViewSet (viewsets.ModelViewSet):
    queryset = Notification.objects.all ()
    serializer_class = NotificationSerializer

    def list (self, request, *args, **kwargs):
        user = request.user
        cache_key = f'notifications_{user.id}'
        notifications = cache.get (cache_key)

        if notifications is None:
            notifications = self.get_queryset ().filter (user=user)
            cache.set (cache_key, notifications, timeout=60 * 5)  # Cache for 5 minutes

        serializer = self.get_serializer (notifications, many=True)
        return Response (serializer.data)

    def retrieve (self, request, pk=None):
        cache_key = f'notification_{pk}'
        notification = cache.get (cache_key)

        if notification is None:
            notification = get_object_or_404 (Notification, pk=pk, user=request.user)
            cache.set (cache_key, notification, timeout=60 * 5)  # Cache for 5 minutes

        serializer = self.get_serializer (notification)
        return Response (serializer.data)

    def create (self, request, *args, **kwargs):
        serializer = self.get_serializer (data=request.data)
        serializer.is_valid (raise_exception=True)
        notification = serializer.save (user=request.user)

        # Clear cache
        cache_key = f'notifications_{request.user.id}'
        cache.delete (cache_key)

        # Send notification to the WebSocket group
        channel_layer = get_channel_layer ()
        async_to_sync (channel_layer.group_send) (
            f"user_{notification.user.id}",  # Group name
            {
                'type': 'send_notification',
                'message': notification.message,  # Adjust as necessary
            }
        )

        return Response (serializer.data)

    def update (self, request, pk=None):
        instance = self.get_object ()
        serializer = self.get_serializer (instance, data=request.data, partial=True)
        serializer.is_valid (raise_exception=True)
        serializer.save ()

        # Clear cache
        cache_key = f'notification_{instance.id}'
        cache.delete (cache_key)

        return Response (serializer.data)

    def create_fake_notification (request):
        """Creates a fake notification and sends it via WebSockets."""
        fake = Faker ()
        user = User.objects.first ()

        if not user:
            return JsonResponse ({"error": "No user found!"}, status=400)

        notification = Notification.objects.create (
            user=user,
            message=fake.sentence (),
            is_read=False,
            notification_type=fake.random_element (elements=('real-time', 'batch', 'email'))
        )

        # Send notification to WebSockets
        channel_layer = get_channel_layer ()
        async_to_sync (channel_layer.group_send) (
            "notifications",
            {
                "type": "send_notification",
                "message": notification.message
            }
        )

        return JsonResponse ({"message": "Notification created and sent in real-time!"})

import json
from channels.generic.websocket import AsyncWebsocketConsumer


r"""

from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class NotificationViewSet (viewsets.ModelViewSet):
    queryset = Notification.objects.all ()
    serializer_class = NotificationSerializer

    def list (self, request, *args, **kwargs):
        user = request.user
        cache_key = f'notifications_{user.id}'
        notifications = cache.get (cache_key)

        if notifications is None:
            notifications = self.get_queryset ().filter (user=user)
            cache.set (cache_key, notifications, timeout=60 * 5)  # Cache for 5 minutes

        serializer = self.get_serializer (notifications, many=True)
        return Response (serializer.data)

    def retrieve (self, request, pk=None):
        cache_key = f'notification_{pk}'
        notification = cache.get (cache_key)

        if notification is None:
            notification = get_object_or_404 (Notification, pk=pk, user=request.user)
            cache.set (cache_key, notification, timeout=60 * 5)  # Cache for 5 minutes

        serializer = self.get_serializer (notification)
        return Response (serializer.data)

    def create (self, request, *args, **kwargs):
        serializer = self.get_serializer (data=request.data)
        serializer.is_valid (raise_exception=True)
        notification = serializer.save (user=request.user)

        # Clear cache
        cache_key = f'notifications_{request.user.id}'
        cache.delete (cache_key)

        return Response (serializer.data)

    def update (self, request, pk=None):
        instance = self.get_object ()
        serializer = self.get_serializer (instance, data=request.data, partial=True)
        serializer.is_valid (raise_exception=True)
        serializer.save ()

        # Clear cache
        cache_key = f'notification_{instance.id}'
        cache.delete (cache_key)

        return Response (serializer.data)



def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    notification = serializer.save(user=request.user)

    # Clear cache
    cache_key = f'notifications_{request.user.id}'
    cache.delete(cache_key)

    # Send notification to the WebSocket group
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{notification.user.id}",  # Group name
        {
            'type': 'send_notification',
            'message': notification.message,  # Adjust as necessary
        }
    )

    return Response(serializer.data)





||||||||||||||||||||||||||||||||||||||||
=====================================
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from rest_framework import generics
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListCreateView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        cache_key = f'notifications_{user.id}'
        notifications = cache.get(cache_key)

        if notifications is None:
            notifications = self.get_queryset().filter(user=user)
            cache.set(cache_key, notifications, timeout=60 * 5)  # Cache for 5 minutes

        return TemplateResponse(request, 'notification_app/notification_list.html', {'notifications': notifications})

    def perform_create(self, serializer):
        notification = serializer.save(user=self.request.user)
        # Clear the cache when a new notification is created
        cache_key = f'notifications_{self.request.user.id}'
        cache.delete(cache_key)







class NotificationRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get(self, request, *args, **kwargs):
        notification_id = kwargs['pk']
        cache_key = f'notification_{notification_id}'
        notification = cache.get(cache_key)

        if notification is None:
            notification = get_object_or_404(Notification, pk=notification_id, user=request.user)
            cache.set(cache_key, notification, timeout=60 * 5)  # Cache for 5 minutes

        return TemplateResponse(request, 'notification_app/notification_detail.html', {'notification': notification})

    def perform_update(self, serializer):
        instance = self.get_object()
        serializer.save()
        # Clear the cache when the notification is updated
        cache_key = f'notification_{instance.id}'
        cache.delete(cache_key)



"""


