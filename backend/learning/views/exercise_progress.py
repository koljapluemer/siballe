from django.db import transaction
from django.utils.dateparse import parse_datetime
from rest_framework.response import Response
from rest_framework.views import APIView

from learning.models import ExerciseProgress
from learning.serializers import ExerciseProgressSerializer


class ExerciseProgressSyncView(APIView):
    """POST /api/sync/exercise-progress/ — push-then-pull-full-state sync.

    Body: {"progress": [{"node_id", "card_data", "updated_at"}, ...]}. Each item is
    applied last-write-wins against the user's stored progress (an incoming item only
    overwrites if its `updated_at` is newer). The response is always the user's
    complete current progress set, not just a delta — simplest correct protocol at
    this data scale (no cursors/versioning needed).
    """

    def post(self, request):
        incoming = ExerciseProgressSerializer(data=request.data.get("progress", []), many=True)
        incoming.is_valid(raise_exception=True)

        for item in incoming.validated_data:
            if parse_datetime(item["card_data"].get("due", "")) is None:
                return Response({"detail": "card_data.due must be a valid datetime"}, status=400)

        with transaction.atomic():
            for item in incoming.validated_data:
                due = parse_datetime(item["card_data"]["due"])
                progress, created = ExerciseProgress.objects.get_or_create(
                    user=request.user,
                    node_id=item["node_id"],
                    defaults={
                        "card_data": item["card_data"],
                        "due": due,
                        "client_updated_at": item["client_updated_at"],
                    },
                )
                if not created and item["client_updated_at"] > progress.client_updated_at:
                    progress.card_data = item["card_data"]
                    progress.due = due
                    progress.client_updated_at = item["client_updated_at"]
                    progress.save(update_fields=["card_data", "due", "client_updated_at"])

        current = ExerciseProgress.objects.filter(user=request.user)
        return Response({"progress": ExerciseProgressSerializer(current, many=True).data})
