import datetime
from django.db import models
from core import models as core_models
from django.utils import timezone
from . import managers


class BookedDay(core_models.TimeStampedModel):

    day = models.DateField()
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Booked Day"
        verbose_name_plural = "Booked Day"

    def __str__(self):

        return str(self.day)


class Reservation(core_models.TimeStampedModel):

    """ Reservation Model Definition """

    class Meta:
        ordering = ("-created",)

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceled"),
    )

    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    check_in = models.DateField()
    check_out = models.DateField(blank=True, null=True, default=0)
    guest = models.ForeignKey(
        "users.User", related_name="reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reservations", on_delete=models.CASCADE
    )
    objects = managers.CustomReservationManager()

    def __str__(self):
        return f"{self.room} - {self.check_in}"

    def in_progress(self):
        now = timezone.now().date()
        return now >= self.check_in and now <= self.check_out

    in_progress.boolean = True  # Admin 패널에서 반환값을 기호로(아이콘으로) 바꿔줌.

    def is_finished(self):
        now = timezone.now().date()
        is_finished = now > self.check_out
        if is_finished:
            BookedDay.objects.filter(reservation=self).delete()
        return is_finished

    is_finished.boolean = True

    def clean(self):  # Seed 때문에 만듬. save 에서 호출.
        if not self.check_out:
            self.check_out = self.check_in + datetime.timedelta(days=1)

    def save(self, *args, **kwargs):
        self.clean()
        # if self.pk is None:
        try:
            kwargs["edit"]
            return super().save()
        except KeyError:
            if True:
                start = self.check_in
                end = self.check_out
                difference = end - start
                existing_booked_day = BookedDay.objects.filter(
                    day__range=(start, start + datetime.timedelta(days=1)),
                    reservation__room=self.room,
                )
                if not existing_booked_day.exists():
                    super().save(*args, **kwargs)
                    for i in range(difference.days + 1):
                        day = start + datetime.timedelta(days=i)
                        BookedDay.objects.create(day=day, reservation=self)
                elif len(existing_booked_day) == 1:
                    super().save(*args, **kwargs)
                    BookedDay.objects.create(day=start, reservation=self)