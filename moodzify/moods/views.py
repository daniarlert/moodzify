from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import MoodEntryForm
from .models import MoodEntry


class UserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    success_url = reverse_lazy("mood_list")

    def test_func(self):
        return self.get_object().user == self.request.user

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy("mood_list"))


class MoodListView(LoginRequiredMixin, ListView):
    model = MoodEntry
    template_name = "moods/mood_list.html"
    context_object_name = "mood_list"

    def get_queryset(self):
        return MoodEntry.objects.filter(user=self.request.user)


class MoodCreateView(LoginRequiredMixin, CreateView):
    template_name = "moods/mood_create.html"
    form_class = MoodEntryForm
    success_url = reverse_lazy("mood_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateView(UserRequiredMixin, UpdateView):
    model = MoodEntry
    template_name = "moods/mood_update.html"
    form_class = MoodEntryForm


class DeleteView(UserRequiredMixin, DeleteView):
    model = MoodEntry
    template_name = "moods/mood_delete.html"
