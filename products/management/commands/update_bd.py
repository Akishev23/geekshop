from django.core.management.base import BaseCommand
from users.models import UserExternProfile, User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            UserExternProfile.objects.create(user=user)
