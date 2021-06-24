from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("login/github/", views.github_login, name="github-login"),
    path("login/github/callback/", views.github_callback, name="github-callback"),
    path("login/kakao/", views.kakao_login, name="kakao-login"),
    path("login/kakao/callback/", views.kakao_callback, name="kakao-callback"),
    path("logout/", views.log_out, name="logout"),
    path("sign-up/", views.SignUpView.as_view(), name="sign-up"),
    path(
        "verify/<str:key>/", views.complete_verification, name="complete-verification"
    ),
    path("<int:pk>/", views.UserProfileView.as_view(), name="profile"),
    path("update-profile/", views.UpdateProfileView.as_view(), name="update"),
    path("update-avatar/", views.UpdateAvatarView.as_view(), name="update-avatar"),
    path("update-avatar-done/", views.update_avatar_done, name="update-avatar-done"),
    path("update-password/", views.UpdatePasswordView.as_view(), name="password"),
    # path("switch_hosting/", views.switch_hosting, name="switch-hosting"),
    path("switch-language/", views.switch_lang, name="switch-language"),
]
