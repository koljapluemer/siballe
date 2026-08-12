from rest_framework import serializers


class ExerciseSerializer(serializers.Serializer):
    id = serializers.IntegerField(source="node_id")
    kind = serializers.ChoiceField(choices=["FlashcardVocab", "FlashcardSentence"])
    front = serializers.CharField()
    back = serializers.CharField()
    credits = serializers.CharField(allow_blank=True)


class ExercisePoolEntrySerializer(ExerciseSerializer):
    """Serializes an (Exercise, situation_ids) pair as produced by generate_exercise_pool."""

    def to_representation(self, instance):
        exercise, situation_ids = instance
        data = super().to_representation(exercise)
        data["situation_ids"] = sorted(situation_ids)
        return data
