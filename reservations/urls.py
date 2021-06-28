from django.urls import path
from . import views

app_name = "reservations"

urlpatterns = [
    path(
        "create/<int:room>/<int:year>-<int:month>-<int:day>/",
        views.create,
        name="create",
    ),
    path("<int:pk>/", views.ReservationDetailView.as_view(), name="detail"),
    path("<int:pk>/<str:verb>/", views.edit_reservation, name="edit"),
    path("my-list/", views.MyReservationsView.as_view(), name="my-list"),
    path(
        "room-reservation/<int:room_pk>/",
        views.RoomReservationView.as_view(),
        name="room-reservation",
    ),
]
