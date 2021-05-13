from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class EmailLoginOnlyView(UserPassesTestMixin):

    """ Check User's login method is Email """

    def test_func(self):
        if self.request.user.login_method == "email":
            return True
        else:
            return False

    def handle_no_permission(self):
        # 마찬가지로 믹스인의 메소드.
        messages.error(self.request, "잘못된 접근입니다.")
        return redirect(reverse("core:home"))


class LoggedOutOnlyView(UserPassesTestMixin):

    """ LoggedOutOnly View Mixin Definition """

    def test_func(self):
        # UserPassesTestMixin 의 메소드. test_func 의 값이 참이 될 때만 다음으로 넘어갈 수 있다.
        # 즉 이 믹스인을 View 에 부모 클래스로 두면, 로그인 했을 때 유저는 View 를 볼 수 없다.
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        # 마찬가지로 믹스인의 메소드.
        messages.error(self.request, "잘못된 접근입니다.")

        return redirect(reverse("core:home"))


class LoggedInOnlyView(LoginRequiredMixin):
    login_url = reverse_lazy("users:login")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request, "로그인 페이지로 이동합니다.")
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
