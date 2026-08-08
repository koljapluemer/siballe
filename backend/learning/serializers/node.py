from rest_framework import serializers

from learning.models import Node
from learning.models.validators import validate_iso639_3


class NodeCandidateSerializer(serializers.Serializer):
    content = serializers.CharField()


class TranslationRowSerializer(serializers.Serializer):
    content = serializers.CharField(allow_blank=True, required=False, default="")
    note = serializers.CharField(allow_blank=True, required=False, default="")


class AddContentRequestSerializer(serializers.Serializer):
    kind = serializers.ChoiceField(choices=Node.Kind.choices)
    language = serializers.CharField(validators=[validate_iso639_3])
    situation_description = serializers.CharField(allow_blank=True, required=False, default="")
    content = serializers.CharField(allow_blank=True, required=False, default="")
    translations = TranslationRowSerializer(many=True, required=False, default=list)
    openai_api_key = serializers.CharField(
        allow_blank=True, required=False, default="", write_only=True
    )

    def validate(self, data):
        has_content = bool(data.get("content", "").strip())
        has_translation = any(
            row.get("content", "").strip() for row in data.get("translations", [])
        )
        if not has_content and not has_translation:
            raise serializers.ValidationError(
                "Provide either the target-language content or at least one translation."
            )
        return data
