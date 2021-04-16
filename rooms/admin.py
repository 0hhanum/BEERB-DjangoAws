from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition """

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("host", "name", "description", "country", "address", "price")},
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")}),
        (
            "Spaces",
            {
                "fields": (
                    "guests",
                    "beds",
                    "bedrooms",
                    "baths",
                )
            },
        ),
        (
            "More About the Space",
            {
                "fields": (
                    "room_type",
                    "amenities",
                    "facilities",
                    "house_rules",
                )
            },
        ),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",  # admin function (아래)
        "count_photos",
    )

    # ordering = ("price",)  # 패널이 로딩되면 바로 무엇을 기준으로 sort 할 것인지 선택.

    list_filter = (
        "instant_book",
        "host__superhost",  # admin 에서 Foreign Key 접근 방식 __
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    search_fields = ("city", "host__username")
    # admin 패널 Room 에서 city 명으로 검색하는 seacrh bar 생성.

    filter_horizontal = (  # ManytoMany Field 에서 수평으로 Filter 사용.
        "amenities",
        "facilities",
        "house_rules",
    )

    # Admin function
    def count_amenities(self, obj):  # self: RoomAdmin 클래스, obj: 패널의 행 (row).

        return obj.amenities.count()  # row 의 amenities 로 접근, 개수를 확인.

    # count_amenities.short_description = "abc"  # 패널 열 (column) 명 지정

    def count_photos(self, obj):
        return obj.photos.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    pass
