from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import MoodEntry


class MoodEntryModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )

        self.mood_entry = MoodEntry.objects.create(
            user=self.user,
            mood_level=1,  # Positive
            notes="Feeling great!",
        )

    def test_mood_entry_creation(self):
        self.assertEqual(self.mood_entry.user, self.user)
        self.assertEqual(self.mood_entry.mood_level, 1)
        self.assertEqual(self.mood_entry.notes, "Feeling great!")

    def test_string_representation(self):
        self.assertEqual(str(self.mood_entry), str(self.mood_entry.timestamp))

    def test_mood_level_choices(self):
        valid_choices = [-2, -1, 0, 1, 2]
        for choice in valid_choices:
            mood_entry = MoodEntry.objects.create(
                user=self.user,
                mood_level=choice,
                notes=f"Test entry with mood level {choice}",
            )
            self.assertIn(mood_entry.mood_level, valid_choices)

    def test_invalid_mood_level_choice(self):
        invalid_choices = [-3, 3, 5]
        for choice in invalid_choices:
            with self.assertRaises(ValidationError):
                mood_entry = MoodEntry(
                    user=self.user,
                    mood_level=choice,
                    notes=f"Test entry with invalid mood level {choice}",
                )
                mood_entry.full_clean()

    def test_timestamp_auto_add(self):
        mood_entry = MoodEntry.objects.create(
            user=self.user,
            mood_level=0,
            notes="Testing timestamp auto add",
        )
        self.assertIsNotNone(mood_entry.timestamp)
