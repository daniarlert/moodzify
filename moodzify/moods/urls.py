from django.urls import path

from .views import DeleteView, MoodCreateView, MoodListView, UpdateView

urlpatterns = [
    path("", MoodListView.as_view(), name="mood_list"),
    path("new/", MoodCreateView.as_view(), name="mood_new"),
    path("<uuid:pk>/edit", UpdateView.as_view(), name="mood_update"),
    path("<uuid:pk>/delete", DeleteView.as_view(), name="mood_delete"),
]
