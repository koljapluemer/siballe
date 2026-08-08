from django.urls import path

from .views.exercises import GenerateExerciseView
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
    path("languages/", LanguageListView.as_view(), name="language-list"),
    path("nodes/search/", NodeSearchView.as_view(), name="node-search"),
    path("nodes/add-content/", AddContentView.as_view(), name="node-add-content"),
]
