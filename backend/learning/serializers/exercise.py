from rest_framework import serializers


class ExerciseSerializer(serializers.Serializer):
    kind = serializers.ChoiceField(choices=["FlashcardVocab", "FlashcardSentence"])
    front = serializers.CharField()
    back = serializers.CharField()
    credits = serializers.CharField(allow_blank=True)
