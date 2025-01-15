from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, notifications_page

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = router.urls  # Store the router-generated URLs first

# Extend urlpatterns instead of overwriting it
urlpatterns += [
    path('notifications/', notifications_page, name='notifications'),
]
