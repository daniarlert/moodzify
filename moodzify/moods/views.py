from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .forms import MoodEntryForm
from .models import MoodEntry


class MoodListView(LoginRequiredMixin, ListView):
    model = MoodEntry
    template_name = "moods/mood_list.html"
    context_object_name = "mood_list"

    def get_queryset(self):
        return MoodEntry.objects.filter(user=self.request.user)


class MoodDetailView(LoginRequiredMixin, UpdateView):
    template_name = "moods/mood_create.html"
    form_class = MoodEntry
    success_url = reverse_lazy("mood_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MoodCreateView(LoginRequiredMixin, CreateView):
    template_name = "moods/mood_create.html"
    form_class = MoodEntryForm
    success_url = reverse_lazy("mood_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MoodUpdateView(LoginRequiredMixin, UpdateView):
    model = MoodEntry
    template_name = "moods/mood_create.html"
    form_class = MoodEntryForm
    success_url = reverse_lazy("mood_list")
