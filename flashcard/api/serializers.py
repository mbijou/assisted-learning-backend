from rest_framework.serializers import ModelSerializer, SerializerMethodField
from flashcard.models import Flashcard


class FlashcardSerializer(ModelSerializer):
    class Meta:
        model = Flashcard
        fields = ("id", "question", "deadline", "workload", "type", "object_id", "rank", "status", "bootstrap_color", )

    type = SerializerMethodField()
    object_id = SerializerMethodField()
    bootstrap_color = SerializerMethodField()

    @staticmethod
    def get_type(instance: Flashcard):
        return instance.content_type.model

    @staticmethod
    def get_object_id(instance: Flashcard):
        return instance.object_id

    @staticmethod
    def get_bootstrap_color(instance: Flashcard):
        status = instance.status

        if status == "DONE":
            return "success"
        elif status == "OPEN":
            return "warning"
        else:
            return "danger"
