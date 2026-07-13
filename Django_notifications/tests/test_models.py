"""Tests for the Notification model and API endpoints.

Run with:  pytest
"""
import pytest
from django.contrib.auth.models import User
from django.core.cache import cache
from django.urls import reverse
from rest_framework.test import APIClient

from notification_app.models import Notification


@pytest.fixture(autouse=True)
def clear_cache():
    """The viewset caches per-user; clear between tests so cached
    querysets from one test cannot leak into the next."""
    cache.clear()
    yield
    cache.clear()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="test-pass-123")


@pytest.fixture
def api_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.mark.django_db
def test_notification_creation(user):
    notification = Notification.objects.create(
        user=user,
        message="Test notification",
        is_read=False,
        notification_type="real-time",
    )
    assert notification.user.username == "testuser"
    assert notification.message == "Test notification"
    assert notification.is_read is False
    assert notification.is_real_time() is True


@pytest.mark.django_db
def test_batch_notification_is_not_real_time(user):
    notification = Notification.objects.create(
        user=user, message="Batch digest", notification_type="batch"
    )
    assert notification.is_real_time() is False


@pytest.mark.django_db
def test_list_requires_authentication():
    response = APIClient().get(reverse("notification-list"))
    assert response.status_code in (401, 403)


@pytest.mark.django_db
def test_list_returns_only_own_notifications(api_client, user):
    other = User.objects.create_user(username="other", password="test-pass-123")
    Notification.objects.create(user=user, message="Mine", notification_type="batch")
    Notification.objects.create(user=other, message="Not mine", notification_type="batch")

    response = api_client.get(reverse("notification-list"))

    assert response.status_code == 200
    messages = [n["message"] for n in response.json()]
    assert messages == ["Mine"]


@pytest.mark.django_db
def test_notification_detail(api_client, user):
    notification = Notification.objects.create(
        user=user, message="Test notification", notification_type="real-time"
    )
    response = api_client.get(reverse("notification-detail", args=[notification.id]))

    assert response.status_code == 200
    assert response.json()["message"] == "Test notification"


@pytest.mark.django_db
def test_detail_of_other_users_notification_is_404(api_client):
    other = User.objects.create_user(username="other", password="test-pass-123")
    notification = Notification.objects.create(
        user=other, message="Not yours", notification_type="batch"
    )
    response = api_client.get(reverse("notification-detail", args=[notification.id]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_create_notification(api_client, user):
    response = api_client.post(
        reverse("notification-list"),
        {"message": "Created via API", "is_read": False},
    )
    assert response.status_code == 200, response.content
    created = Notification.objects.get(message="Created via API")
    assert created.user == user
