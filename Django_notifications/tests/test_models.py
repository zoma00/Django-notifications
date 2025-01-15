import pytest
from django.urls import reverse
from notification_app.models import Notification
from django.contrib.auth.models import User


@pytest.mark.django_db  # This marker allows access to the database for the test
def test_notification_creation ():
    user = User.objects.create (username='testuser')
    notification = Notification.objects.create (
        user=user,
        message='Test notification',
        read=False
    )

    assert notification.user.username == 'testuser'
    assert notification.message == 'Test notification'
    assert notification.read is False


@pytest.mark.django_db
def test_notification_detail_view (client):
    user = User.objects.create (username='testuser')
    notification = Notification.objects.create (
        user=user,
        message='Test notification',
        read=False
    )

    url = reverse ('notification-retrieve-update', args=[notification.id])
    response = client.get (url)

    assert response.status_code == 200
    assert 'Test notification' in str (response.content)
