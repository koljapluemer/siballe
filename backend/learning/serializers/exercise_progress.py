from rest_framework import serializers


class ExerciseProgressSerializer(serializers.Serializer):
    node_id = serializers.IntegerField()
    card_data = serializers.JSONField()
    updated_at = serializers.DateTimeField(source="client_updated_at")
