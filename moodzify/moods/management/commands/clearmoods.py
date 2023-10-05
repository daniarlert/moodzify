from django.core.management.base import BaseCommand
from moods.models import MoodEntry


class Command(BaseCommand):
    help = "Delete all MoodEntry instances from the database."

    def handle(self, *args, **options):
        MoodEntry.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS("All MoodEntry objects deleted from the database.")
        )
