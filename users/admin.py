from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# Register your models here.

# admin.site.register(models.User, CustomUserAdmin)  이렇게 할 수도 있음


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    # class CustomUserAdmin(admin.ModelAdmin):
    # 이렇게 하는 방법도 있음. 그러나 장고에서 제공해주는 userAdmin 전용 패널을 사용할 것임.

    """ Custom User Admin """

    # list_display = (
    #     "username",
    #     "gender",
    #     "language",
    #     "currency",
    #     "superhost",
    # )  user list 에서 항목을 보여주는 옵션

    # list_filter = (
    #     "superhost",
    #     "language",
    #  filter 를 만드는 옵션

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
