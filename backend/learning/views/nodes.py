from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from learning.models import Node
from learning.serializers import AddContentRequestSerializer, NodeCandidateSerializer
from learning.services.content_creation import add_content

SEARCH_RESULT_LIMIT = 20


class NodeSearchView(APIView):
    """GET /api/nodes/search/?kind=&language=&q= — autocomplete candidates."""

    permission_classes = [AllowAny]

    def get(self, request):
        kind = request.query_params.get("kind")
        language = request.query_params.get("language")
        query = request.query_params.get("q", "")

        if kind not in Node.Kind.values or not language:
            return Response({"detail": "kind and language are required"}, status=400)
        if not query.strip():
            return Response([])

        nodes = Node.objects.filter(
            kind=kind, language=language, content__icontains=query.strip()
        ).order_by("content")[:SEARCH_RESULT_LIMIT]
        return Response(NodeCandidateSerializer(nodes, many=True).data)


class AddContentView(APIView):
    """POST /api/nodes/add-content/ — save a new Node (+ translations, situation link)."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AddContentRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        result = add_content(
            kind=data["kind"],
            language=data["language"],
            situation_description=data["situation_description"],
            content=data["content"],
            translations=data["translations"],
            api_key=data["openai_api_key"],
        )
        return Response(result.as_dict(), status=201)
