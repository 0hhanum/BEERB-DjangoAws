from django.contrib import admin
from django.utils.html import mark_safe
from . import models

# Register your models here.


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()


class PhotoInline(admin.TabularInline):  # Admin 안에 Admin 을 만들어주는 inline admin

    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition """

    inlines = (PhotoInline,)

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "host",
                    "name",
                    "description",
                    "country",
                    "city",
                    "address",
                    "price",
                )
            },
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
        "total_rating",
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

    raw_id_fields = ("host",)  # user 엄청 많아지게 되면 스크롤로 찾는 거 효율 떨어짐. foreingKey 찾는 방법.
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

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(
            f'<img width="40px" style="border-radius: 7px" height=40px src="{obj.file.url}"/>'
        )
        # mark safe = selenium execute_script 같은거.

    get_thumbnail.short_description = "Thumbnail"
