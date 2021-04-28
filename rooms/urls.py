from django.urls import path
from . import views


app_name = "rooms"

urlpatterns = [
    path("<int:pk>", views.RoomDetail.as_view(), name="detail"),  # pk 라는 이름 부여해준것.
    path("search/", views.SearchView.as_view(), name="search"),
]
