from rest_framework import serializers

from learning.models import Situation


class SituationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Situation
        fields = ["id", "description"]


class LanguageGroupSerializer(serializers.Serializer):
    language = serializers.CharField()
    situations = SituationSerializer(many=True)
