from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from rooms import models as room_models

# Register your models here.

# admin.site.register(models.User, CustomUserAdmin)  이렇게 할 수도 있음


class RoomInline(admin.TabularInline):  # Admin 안에 Admin 을 만들어주는 inline admin
    model = room_models.Room


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    # class CustomUserAdmin(admin.ModelAdmin):
    # 이렇게 하는 방법도 있음. 그러나 장고에서 제공해주는 userAdmin 전용 패널을 사용할 것임.

    """ Custom User Admin """

    inlines = (RoomInline,)

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                ),
            },
        ),
    )

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
    )
    list_filter = UserAdmin.list_filter + ("superhost",)
