from django.urls import path

from .views import MoodEntryList

urlpatterns = [
    path("", MoodEntryList.as_view(), name="mood_entry_list"),
]
