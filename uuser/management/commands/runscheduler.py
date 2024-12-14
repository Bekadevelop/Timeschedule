from django.core.management.base import BaseCommand
from uuser.scheduler import start

class Command(BaseCommand):
    help = 'Starts the APScheduler for periodic tasks'

    def handle(self, *args, **options):
        start()
