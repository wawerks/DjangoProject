from django.core.management.base import BaseCommand
from a_rtchat.models import ChatGroup

class Command(BaseCommand):
    help = 'Creates the public chat group'

    def handle(self, *args, **kwargs):
        ChatGroup.objects.get_or_create(group_name="public-chat")
        self.stdout.write(self.style.SUCCESS('Successfully created public chat group'))
