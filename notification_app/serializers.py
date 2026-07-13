from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'user', 'message', 'is_read', 'created_at')
        # The viewset assigns user from the authenticated request
        read_only_fields = ('user',)
