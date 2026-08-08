from django.urls import path

from .views.exercises import GenerateExerciseView
from .views.situations import SituationListView

urlpatterns = [
    path("situations/", SituationListView.as_view(), name="situation-list"),
    path(
        "exercises/generate/",
        GenerateExerciseView.as_view(),
        name="exercise-generate",
    ),
]
