import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from moods.models import MoodEntry


class Command(BaseCommand):
    help = "Add random MoodEntry objects to the database."

    def add_arguments(self, parser):
        parser.add_argument("num_entries", type=int)

    def handle(self, *args, **options):
        user_queryset = get_user_model().objects.all()
        num_entries = options["num_entries"]
        random_entries = [
            MoodEntry(
                user=random.choice(user_queryset),
                mood_level=random.choice(
                    [choice[0] for choice in MoodEntry.MOOD_LEVEL_CHOICES]
                ),
                notes=f"Random note for entry {i + 1}",
            )
            for i in range(num_entries)
        ]

        MoodEntry.objects.bulk_create(random_entries)
        self.stdout.write(
            self.style.SUCCESS("random MoodEntry objects added to the database.")
        )
