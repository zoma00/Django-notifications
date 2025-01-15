from django.core.management.base import BaseCommand
from notification_app.models import Notification
from django.contrib.auth.models import User
from faker import Faker
import random

class Command(BaseCommand):
    help = "Generate fake notifications"

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of notifications to create')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        fake = Faker()
        users = list(User.objects.all())  # Get all users

        if not users:
            self.stdout.write(self.style.ERROR('No users found. Please create some users first.'))
            return

        for _ in range(count):
            user = random.choice(users)  # Select a random user
            Notification.objects.create(
                user=user,
                message=fake.sentence(),
                is_read=fake.boolean(),
                notification_type=fake.random_element(elements=('real-time', 'batch', 'email'))
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} fake notifications!'))





