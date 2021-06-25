from django.shortcuts import redirect, reverse
from django.contrib import messages
from django.views.generic import TemplateView
from rooms import models as room_models
from . import models


def toggle_room(request, room_pk):

    if request.user.is_authenticated is False:
        messages.error(request, "로그인 후 이용하세요.")
        return redirect(reverse("users:login"))
    room = room_models.Room.objects.get_or_none(pk=room_pk)
    action = request.GET.get("action", None)
    if room is not None and action is not None:
        the_list, _ = models.List.objects.get_or_create(
            user=request.user, name="My Favorites Houses"
        )

        if action == "add":
            the_list.rooms.add(room)
        elif action == "remove":
            the_list.rooms.remove(room)
    return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))


class SeeFavsView(TemplateView):

    template_name = "lists/list_detail.html"
