# from django.views import View
import os
import requests

from django.views.generic import DetailView, UpdateView, FormView
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, reverse, render
from django.contrib.auth import authenticate, login, logout

# from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.base import ContentFile
from django.contrib.messages.views import SuccessMessageMixin
from . import forms, models, mixins


"""class LoginView(View):
    def get(self, request):

        form = forms.LoginForm(initial={"email": "asdf@dsaf.com"})
        return render(request, "users/login.html", context={"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("core:home"))

        return render(request, "users/login.html", context={"form": form})"""


# Using formView
class LoginView(mixins.LoggedOutOnlyView, FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    initial = {"email": "asdf@dsaf.com"}

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(
                self.request, f"{user.first_name} {user.last_name}님, 환영합니다!"
            )

        return super().form_valid(form)


def log_out(request):
    user = request.user
    logout(request)
    messages.info(request, f"See you later {user.first_name}!")
    return redirect(reverse("core:home"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):

    template_name = "users/sign_up.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):

        form.save()

        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            login(self.request, user)
            messages.success(
                self.request, f"{user.first_name} {user.last_name}님, 환영합니다!"
            )
            # user.verify_email()

        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
    except models.User.DoesNotExist:
        pass

    return redirect(reverse("core:home"))


def github_login(request):

    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get("code", None)

        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                raise GithubException("잘못된 접근입니다.")
            else:
                access_token = token_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = profile_request.json()
                email = profile_json.get("email", None)

                if email is not None:
                    name = profile_json.get("login")
                    email = profile_json.get("email")
                    bio = profile_json.get("bio")

                    if bio is None:
                        bio = "none"

                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException(
                                f"잘못된 접근입니다. {user.login_method}를 이용해 로그인하세요."
                            )

                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        user.set_unusable_password()
                        user.save()

                    login(request, user)
                    messages.success(
                        request, f"{user.first_name} {user.last_name}님, 환영합니다!"
                    )
                    return redirect(reverse("core:home"))

                else:
                    raise GithubException(
                        "Github 에 이메일이 등록되어있지 않습니다. 다른 로그인 방법을 이용하세요."
                    )
        else:
            raise GithubException("잘못된 접근입니다.")
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


def kakao_login(request):
    app_key = os.environ.get("KAKAO_KEY")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={app_key}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoException(Exception):

    pass


def kakao_callback(request):

    app_key = os.environ.get("KAKAO_KEY")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"

    try:
        code = request.GET.get("code")
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={app_key}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = token_request.json()
        error = token_json.get("error", None)

        if error is not None:
            raise KakaoException("잘못된 접근입니다.")
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        email = profile_json.get("kakao_account", None).get("email", None)
        if not email:
            raise KakaoException("이메일 수집 동의에 체크해주세요.")

        properties = profile_json.get("properties")
        nickname = properties.get("nickname")
        profile_image = properties.get("profile_image")

        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException(f"잘못된 접근입니다. {user.login_method} 를 이용해 로그인하세요.")

        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()

            if profile_image is not None:
                photo_request = requests.get(profile_image)
                user.avatar.save(
                    f"{nickname}-avatar", ContentFile(photo_request.content)
                )
                # content() 는 binary 로 image 를 변환, ContentFile 은 binary 를 읽어줌
                # save 는 ImageField 의 저장 메소드
        login(request, user)
        messages.success(request, f"{user.first_name} {user.last_name}님, 환영합니다!")
        return redirect(reverse("core:home"))

    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):

    """ User Profile View Description """

    model = models.User
    context_object_name = "user_obj"


class UpdateProfileView(SuccessMessageMixin, mixins.LoggedInOnlyView, UpdateView):

    model = models.User
    template_name = "users/update_profile.html"
    fields = (
        "first_name",
        "last_name",
        "gender",
        "bio",
        "language",
        "currency",
    )
    success_message = "변경 완료!"

    def get_object(self, queryset=None):

        return self.request.user


class UpdateAvatarView(UpdateView):

    """ Update Avatar View Description """

    model = models.User
    template_name = "users/update_avatar.html"
    fields = ("avatar",)
    success_url = reverse_lazy("users:update-avatar-done")

    def get_object(self, queryset=None):

        return self.request.user


def update_avatar_done(request):

    return render(request, "update_done.html")


class UpdatePasswordView(
    SuccessMessageMixin,
    mixins.EmailLoginOnlyView,
    mixins.LoggedInOnlyView,
    PasswordChangeView,
):

    template_name = "users/update_password.html"
    success_message = "변경 완료!"

    def get_success_url(self):
        return reverse("users:profile", kwargs={"pk": self.request.user.pk})


# @login_required
# def switch_hosting(request):
#     try:
#         del request.session["is_hosting"]
#         messages.success(request, "게스트 모드입니다.")

#     except KeyError:
#         messages.success(request, "호스트 모드입니다.")
#         request.session["is_hosting"] = True

#     return redirect(reverse_lazy("core:home"))
