from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import MoodEntry


class MoodEntryList(LoginRequiredMixin, ListView):
    model = MoodEntry
    template_name = "mood_tracking/mood_list.html"
    context_object_name = "mood_entries"

    def get_queryset(self):
        return MoodEntry.objects.filter(user=self.request.user)
