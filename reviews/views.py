from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.http import Http404
from rooms import models as room_models
from . import forms


def create_review(request, room, reservation):

    if request.method == "POST":
        form = forms.CreateReviewForm(request.POST)
        room = room_models.Room.objects.get_or_none(pk=room)
        if not room:
            return redirect(reverse("core:home"))

        if form.is_valid():
            review = form.save()
            review.room = room
            review.user = request.user
            review.save()
            messages.warning(request, "리뷰 등록 완료!")
            return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))
        else:
            raise Http404()
