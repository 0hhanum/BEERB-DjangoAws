from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.log_out, name="logout"),
    path("sign-up", views.SignUpView.as_view(), name="sign-up"),
    path("verify/<str:key>", views.complete_verification, name="complete-verification"),
]
