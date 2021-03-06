import datetime
from django.http import Http404
from django.views.generic import View, TemplateView
from django.contrib import messages
from django.shortcuts import redirect, reverse, render
from django.urls import NoReverseMatch
from rooms import models as room_models
from reviews import forms as review_forms
from users.mixins import LoggedInOnlyView
from . import models


class CreateError(Exception):
    pass


def create(request, room, year, month, day):

    try:
        date_obj = datetime.datetime(year=year, month=month, day=day)
        room = room_models.Room.objects.get(pk=room)
        models.BookedDay.objects.get(day=date_obj, reservation__room=room)
        raise CreateError()

    except (room_models.Room.DoesNotExist, CreateError):
        messages.error(request, "예약할 수 없습니다.")
        return redirect(reverse("core:home"))

    except models.BookedDay.DoesNotExist:

        if request.user.is_anonymous:
            messages.error(request, "로그인 후 이용하세요.")
            return redirect(reverse("users:login"))
        elif request.user == room.host:
            messages.error(request, "잘못된 접근입니다.")
            return redirect(reverse("core:home"))

        reservation = models.Reservation.objects.create(
            guest=request.user, room=room, check_in=date_obj
        )
        messages.warning(request, "예약 완료! 감사합니다")
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


class ReservationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        reservation = models.Reservation.objects.get_or_none(pk=pk)
        if not reservation:
            messages.error(self.request, "잘못된 접근입니다.")
            return redirect(reverse("core:home"))

        if (
            reservation.guest != self.request.user
            and reservation.room.host != self.request.user
        ):
            raise Http404()

        form = review_forms.CreateReviewForm()
        return render(
            self.request,
            "reservations/detail.html",
            {"reservation": reservation, "form": form},
        )


class RoomReservationView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("room_pk")
        room = room_models.Room.objects.get_or_none(pk=pk)
        if not room:
            messages.error(self.request, "잘못된 접근입니다.")
            return redirect(reverse("core:home"))

        if room.host != self.request.user:
            messages.error(self.request, "잘못된 접근입니다.")
            return redirect(reverse("core:home"))

        return render(
            self.request, "reservations/room_reservation.html", {"room": room}
        )


def edit_reservation(request, pk, verb):
    reservation = models.Reservation.objects.get_or_none(pk=pk)
    if not reservation:
        messages.error(request, "잘못된 접근입니다.")
        return redirect(reverse("core:home"))

    if reservation.guest != request.user and reservation.room.host != request.user:
        raise Http404()

    if verb == "confirm":
        reservation.status = models.Reservation.STATUS_CONFIRMED
        messages.warning(request, "승인 완료!")
    elif verb == "cancel":
        reservation.status = models.Reservation.STATUS_CANCELED
        models.BookedDay.objects.filter(reservation=reservation).delete()
        messages.error(request, "예약 취소되었습니다.")

    reservation.save(edit=True)
    return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


class MyReservationsView(LoggedInOnlyView, TemplateView):

    template_name = "reservations/my_reservation_list.html"
