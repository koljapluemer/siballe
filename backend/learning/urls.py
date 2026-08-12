from django.urls import path

from .views.auth import MeView
from .views.exercise_progress import ExerciseProgressSyncView
from .views.exercises import ExercisePoolView, GenerateExerciseView
from .views.languages import LanguageListView
from .views.nodes import AddContentView, NodeSearchView
from .views.situations import SituationListView

urlpatterns = [
    path("situations/", SituationListView.as_view(), name="situation-list"),
    path(
        "exercises/generate/",
        GenerateExerciseView.as_view(),
        name="exercise-generate",
    ),
    path("exercises/pool/", ExercisePoolView.as_view(), name="exercise-pool"),
    path("languages/", LanguageListView.as_view(), name="language-list"),
    path("nodes/search/", NodeSearchView.as_view(), name="node-search"),
    path("nodes/add-content/", AddContentView.as_view(), name="node-add-content"),
    path("auth/me/", MeView.as_view(), name="auth-me"),
    path(
        "sync/exercise-progress/",
        ExerciseProgressSyncView.as_view(),
        name="exercise-progress-sync",
    ),
]
