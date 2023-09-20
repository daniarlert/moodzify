from django.urls import path

from .views import MoodCreateView, MoodDeleteView, MoodListView, MoodUpdateView

urlpatterns = [
    path("", MoodListView.as_view(), name="mood_list"),
    path("new/", MoodCreateView.as_view(), name="mood_new"),
    path("<uuid:pk>/edit", MoodUpdateView.as_view(), name="mood_update"),
    path("<uuid:pk>/delete", MoodDeleteView.as_view(), name="mood_delete"),
]
