from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from learning.models import Situation
from learning.serializers import ExerciseSerializer
from learning.services.exceptions import NoExercisableContent
from learning.services.exercise_generation import generate_exercise_for_situation


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
