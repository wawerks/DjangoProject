from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from a_users.models import Profile

class Command(BaseCommand):
    help = 'Creates user profiles for users that do not have one'

    def handle(self, *args, **options):
        users_without_profile = User.objects.filter(profile__isnull=True)
        for user in users_without_profile:
            Profile.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Created profile for user: {user.username}'))
