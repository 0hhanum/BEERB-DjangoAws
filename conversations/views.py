from django.db.models import Q
from django.shortcuts import redirect, reverse
from django.views.generic import DetailView
from users import models as user_models
from . import models


def go_conversation(request, a_pk, b_pk):

    try:
        user_one = user_models.User.objects.get(pk=a_pk)
        print(user_one.first_name)
    except user_models.User.DoesNotExist:
        user_one = None
    try:
        user_two = user_models.User.objects.get(pk=b_pk)
        print(user_two)
    except user_models.User.DoesNotExist:
        user_two = None

    if user_one is not None and user_two is not None:
        try:
            conversation = models.Conversation.objects.get(
                Q(participants=user_one) & Q(participants=user_two)
            )
            print(conversation)

        except models.Conversation.DoesNotExist:
            conversation = models.Conversation.objects.create()
            conversation.participants.add(user_one, user_two)

        return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}))


class ConversationDetailView(DetailView):

    model = models.Conversation
