from django.contrib.auth import get_user_model
from django.db import models


class MoodEntry(models.Model):
    MOOD_LEVEL_CHOICES = (
        (-2, "Very Negative"),
        (-1, "Negative"),
        (0, "Neutral"),
        (1, "Positive"),
        (2, "Very Positive"),
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    mood_level = models.IntegerField(
        choices=MOOD_LEVEL_CHOICES, blank=False, null=False
    )
    notes = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp}"
