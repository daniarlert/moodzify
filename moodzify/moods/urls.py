from django.urls import path

from .views import MoodCreateView, MoodDetailView, MoodListView, MoodUpdateView

urlpatterns = [
    path("", MoodListView.as_view(), name="mood_list"),
    path("<uuid:id>/", MoodDetailView.as_view(), name="mood_detail"),
    path("new/", MoodCreateView.as_view(), name="mood_new"),
    path("update/<uuid:pk>/", MoodUpdateView.as_view(), name="mood_update"),
]
