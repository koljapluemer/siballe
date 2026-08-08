import pycountry
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from learning.serializers import LanguageSerializer


class LanguageListView(APIView):
    """GET /api/languages/ — every ISO 639-3 language, for the language picker."""

    permission_classes = [AllowAny]

    def get(self, request):
        languages = sorted(
            ({"code": lang.alpha_3, "name": lang.name} for lang in pycountry.languages),
            key=lambda entry: entry["name"],
        )
        return Response(LanguageSerializer(languages, many=True).data)
