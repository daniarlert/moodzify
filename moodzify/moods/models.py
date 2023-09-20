import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class MoodEntry(models.Model):
    MOOD_LEVEL_CHOICES = (
        (-2, "Very Negative"),
        (-1, "Negative"),
        (0, "Neutral"),
        (1, "Positive"),
        (2, "Very Positive"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    mood_level = models.IntegerField(
        choices=MOOD_LEVEL_CHOICES, blank=False, null=False
    )
    notes = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("mood_detail", args=[str(self.id)])

    def __str__(self):
        return f"{self.timestamp}"
