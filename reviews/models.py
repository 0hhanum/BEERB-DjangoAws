from django.db import models
from core import models as core_models


class Review(core_models.TimeStampedModel):

    """ Review Model Definition """

    review = models.TextField()
    accuracy = models.IntegerField()
    communication = models.IntegerField()
    location = models.IntegerField()
    check_in = models.IntegerField()
    value = models.IntegerField()
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reviews", on_delete=models.CASCADE
    )

    def __str__(self):

        return f"{self.review} - {self.room}"
        # ForeignKey 를 사용했기 때문에 연결된 model 속 field 도 찾을 수 있음!

    def rating_average(self):  # Custom Model Function
        avg = (
            self.accuracy
            + self.communication
            + self.location
            + self.check_in
            + self.value
        ) / 5
        return round(avg, 2)

    rating_average.short_description = "Average"  # 패널에 추가했을때 column 명.