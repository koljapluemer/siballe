from collections import defaultdict

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from learning.models import Situation
from learning.serializers import LanguageGroupSerializer, SituationSerializer


class SituationListView(APIView):
    """GET /api/situations/ — all situations, grouped by language."""

    permission_classes = [AllowAny]

    def get(self, request):
        situations = Situation.objects.order_by("language", "description")
        language = request.query_params.get("language")
        if language:
            situations = situations.filter(language=language)
        grouped: dict[str, list[Situation]] = defaultdict(list)
        for situation in situations:
            grouped[situation.language].append(situation)

        data = [
            {
                "language": language,
                "situations": SituationSerializer(items, many=True).data,
            }
            for language, items in sorted(grouped.items())
        ]
        return Response(LanguageGroupSerializer(data, many=True).data)
