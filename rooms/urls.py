from django.urls import path
from . import views


app_name = "rooms"

urlpatterns = [
    path("<int:pk>/", views.RoomDetail.as_view(), name="detail"),  # pk 라는 이름 부여해준것.
    path("<int:pk>/edit/", views.EditRoomView.as_view(), name="edit"),
    path("<int:pk>/photos/", views.RoomPhotosView.as_view(), name="photos"),
    path(
        "<int:room_pk>/photos/<int:photo_pk>/delete",
        views.delete_photo,
        name="del-photo",
    ),
    path("search/", views.SearchView.as_view(), name="search"),
]
