from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from learning.models import Situation
from learning.serializers import ExercisePoolEntrySerializer, ExerciseSerializer
from learning.services.exceptions import NoExercisableContent
from learning.services.exercise_generation import (
    generate_exercise_for_situation,
    generate_exercise_pool,
)


class GenerateExerciseView(APIView):
    """GET /api/exercises/generate/?situation_id=<id> — a random exercise for the situation."""

    permission_classes = [AllowAny]

    def get(self, request):
        situation_id = request.query_params.get("situation_id")
        if not situation_id:
            return Response({"detail": "situation_id is required"}, status=400)
        try:
            situation_id = int(situation_id)
        except ValueError:
            return Response({"detail": "situation_id must be an integer"}, status=400)

        situation = get_object_or_404(Situation, pk=situation_id)
        try:
            exercise = generate_exercise_for_situation(situation)
        except NoExercisableContent:
            return Response({"detail": "no_exercisable_content"}, status=404)

        return Response(ExerciseSerializer(exercise).data)


class ExercisePoolView(APIView):
    """GET /api/exercises/pool/?situation_ids=1,2,3 — one exercise per eligible node
    across the given situations, for offline caching. No pagination yet — the content
    graph is fixture-scale today; add `updated_since`/paging if that changes."""

    permission_classes = [AllowAny]

    def get(self, request):
        raw_ids = request.query_params.get("situation_ids")
        if not raw_ids:
            return Response({"detail": "situation_ids is required"}, status=400)
        try:
            situation_ids = [int(v) for v in raw_ids.split(",") if v]
        except ValueError:
            return Response(
                {"detail": "situation_ids must be a comma-separated list of integers"},
                status=400,
            )

        situations = list(Situation.objects.filter(pk__in=situation_ids))
        pool = generate_exercise_pool(situations)
        return Response({"results": ExercisePoolEntrySerializer(pool, many=True).data})
