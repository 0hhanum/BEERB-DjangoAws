from django.utils import timezone
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from core import models as core_models
from cal import Calendar

# Create your models here.


class AbstractItem(core_models.TimeStampedModel):

    """Abstract Item"""

    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True  # 데이터베이스에서 참조하지 않는 것. admin 패널에서 확인하는 것과는 다른 문제.


class RoomType(AbstractItem):

    """RoomType Object Definition"""

    class Meta:
        verbose_name = "Room Type"
        # ordering = ["created"]
        # AbstractItem 의 create (core 의 TimeStampedModel) 시간 순서대로 정렬.


class Amenity(AbstractItem):

    """AmenityType Object Definition"""

    class Meta:
        verbose_name_plural = "Amenities"

        # admin 패널에서 자동으로 Amenitys 로 표기되는 걸 커스텀 하기.


class Facility(AbstractItem):

    """Facility Model Definition"""

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):

    """HouseRule Model Definition"""

    class Meta:
        verbose_name_plural = "House Rule"


class Photo(core_models.TimeStampedModel):

    """Photo Model Definition"""

    caption = models.CharField(max_length=80, verbose_name="설명")
    file = models.ImageField(
        upload_to="room-photos", verbose_name="파일"
    )  # media root 안의 어떤 폴더에 저장할 건지 설정.
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)
    # "Room" 처리한 이유는 Room 클래스가 아래에 있기 떄문에 Photo 를 아래로 옮기거나 string 처리해서 읽을 수 있음. 장고의 기능.

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """Room Model Definition"""

    class Meta:
        ordering = ("-created",)

    name = models.CharField(max_length=140, verbose_name="숙소명")
    description = models.TextField(verbose_name="설명")
    country = CountryField(verbose_name="국가")
    city = models.CharField(max_length=80, verbose_name="도시")
    price = models.IntegerField(verbose_name="요금")
    address = models.CharField(max_length=140, verbose_name="주소")
    guests = models.IntegerField(
        help_text="How many people will staying?", verbose_name="최대 가능 게스트 수"
    )
    beds = models.IntegerField(verbose_name="침대 개수")
    bedrooms = models.IntegerField(verbose_name="방 개수")
    baths = models.IntegerField(verbose_name="화장실 개수")
    check_in = models.TimeField(verbose_name="체크인")
    check_out = models.TimeField(verbose_name="체크아웃")
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )
    # foreignKey 는 many to one 구조. 방은 host 를 한 명 밖에 가질 수 없지만 host 는 여러 room 을 가질 수 있음.
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    # many to many 구조를 사용해야할 때는 ManyToManyField 를 사용한다.
    amenities = models.ManyToManyField(
        "Amenity", related_name="rooms", blank=True, verbose_name="편의시설"
    )
    facilities = models.ManyToManyField(
        "Facility", related_name="rooms", blank=True, verbose_name="기타"
    )
    house_rules = models.ManyToManyField(
        "HouseRule", related_name="rooms", blank=True, verbose_name="주의사항"
    )

    def get_absolute_url(self):

        return reverse("rooms:detail", kwargs={"pk": self.pk})

    # admin 에서 detail 에 해당하는 url 로 바로 접근 (view on site 이용)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)

    def total_rating(self):
        all_reviews = self.reviews.all()
        # Review 가 room 을 참조할 때 key "reviews" 를 이용한거임. 역참조 관계 생각.
        all_ratings = 0
        if len(all_reviews) != 0:

            for review in all_reviews:

                all_ratings += review.rating_average()

            return round(all_ratings / len(all_reviews), 1)

        else:
            return "0.0"

    def first_photo(self):
        try:
            photo = self.photos.all()[0]
        except IndexError:
            return None

        return photo.file.url

    def get_next_photos(self):
        default_photo = Photo.objects.get(caption="Default")

        photos = self.photos.all()[1:]
        if len(photos) >= 4:
            photos = photos[:4]
        else:
            while len(photos) < 4:
                photos = list(photos)
                photos.append(default_photo)

        return photos

    def get_calendars(self):

        now = timezone.now()
        this_month_cal = Calendar(now.year, now.month)
        if now.month != 12:
            next_month_cal = Calendar(now.year, now.month + 1)
        else:
            next_month_cal = Calendar(now.year, 1)
        calendars = [this_month_cal, next_month_cal]

        return enumerate(calendars)
