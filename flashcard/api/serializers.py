from rest_framework.serializers import ModelSerializer, SerializerMethodField
from flashcard.models import Flashcard


class FlashcardSerializer(ModelSerializer):
    class Meta:
        model = Flashcard
        fields = ("id", "question", "deadline", "workload", "type", "object_id", "rank", )

    type = SerializerMethodField()
    object_id = SerializerMethodField()

    def get_type(self, instance: Flashcard):
        return instance.content_type.model

    def get_object_id(self, instance: Flashcard):
        return instance.object_id
