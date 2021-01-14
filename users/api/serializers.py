from rest_framework import serializers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", )


class UserAccomplishmentSerializer(serializers.ModelSerializer):
    amount_flashcards_done = serializers.IntegerField()
    amount_flashcards_open = serializers.IntegerField()
    amount_flashcards_expired = serializers.IntegerField()
    percentage_flashcards_total = serializers.IntegerField()
    percentage_flashcards_done = serializers.FloatField()
    percentage_flashcards_open = serializers.FloatField()
    percentage_flashcards_expired = serializers.FloatField()

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "amount_flashcards_done",
                  "amount_flashcards_open", "amount_flashcards_expired", "percentage_flashcards_total",
                  "percentage_flashcards_done", "percentage_flashcards_open", "percentage_flashcards_expired",
                  )


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        user_data = {"first_name": user.first_name, "last_name": user.last_name, "username": user.username,
                     "email": user.email, "id": user.id
                     }

        return Response({
            'token': token.key, 'user': user_data
        })
