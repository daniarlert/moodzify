from django.forms import ModelForm

from .models import MoodEntry


class MoodEntryForm(ModelForm):
    class Meta:
        model = MoodEntry
        fields = ["mood_level", "notes"]
