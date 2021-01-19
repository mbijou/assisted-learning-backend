from django.db.models import Count, Q, Sum, F, FloatField
from django.db.models.functions import Cast
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from users.api.serializers import UserSerializer, UserAccomplishmentSerializer
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
# User = get_user_model()
from django.contrib.auth.models import User
from django.utils.timezone import now


class UserViewSet(ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(detail=True, url_path="users-and-accomplishments")
    def get_users_and_accomplishments(self, request, pk=None):
        user = self.get_users_and_accomplishments_object()
        self.queryset = self.get_users_and_accomplishments_queryset()
        serializer = UserAccomplishmentSerializer(instance=user)
        return Response(serializer.data)

    def get_users_and_accomplishments_object(self):
        queryset = self.filter_queryset(self.get_users_and_accomplishments_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def get_users_and_accomplishments_queryset(self):

        amount_flashcards_done = Count('flashcard__id', filter=Q(flashcard__workload=0))
        amount_flashcards_open = Count(
            'flashcard__id', filter=Q(flashcard__workload__gt=0, flashcard__deadline__gt=now().date())
        )
        amount_flashcards_expired = Count(
            'flashcard__id', filter=Q(flashcard__deadline__lt=now().date(), flashcard__workload__gt=0)
        )

        percentage_flashcards_total = Count('flashcard__id')
        percentage_flashcards_done = Cast(
            Cast(F('amount_flashcards_done'), output_field=FloatField()) /
            Cast(F('percentage_flashcards_total'), output_field=FloatField()) * 100,
            output_field=FloatField()
        )

        percentage_flashcards_open = Cast(
            Cast(F('amount_flashcards_open'), output_field=FloatField()) /
            Cast(F('percentage_flashcards_total'), output_field=FloatField()) * 100,
            output_field=FloatField()
        )

        percentage_flashcards_expired = Cast(
            Cast(F('amount_flashcards_expired'), output_field=FloatField()) /
            Cast(F('percentage_flashcards_total'), output_field=FloatField()) * 100,
            output_field=FloatField()
        )

        self.queryset = self.queryset.annotate(
            amount_flashcards_done=amount_flashcards_done, amount_flashcards_open=amount_flashcards_open,
            amount_flashcards_expired=amount_flashcards_expired).annotate(
            percentage_flashcards_total=percentage_flashcards_total,
            percentage_flashcards_done=percentage_flashcards_done,
            percentage_flashcards_open=percentage_flashcards_open,
            percentage_flashcards_expired=percentage_flashcards_expired
        ).distinct()

        return self.queryset
