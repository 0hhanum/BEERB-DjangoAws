from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.contrib.auth.mixins import UserPassesTestMixin


class RoomHostOnlyView(UserPassesTestMixin):

    """ Check Room's host for edit room """

    def test_func(self):

        host = self.get_object().host
        if self.request.user == host:
            return True
        else:
            return False

    def handle_no_permission(self):
        # 마찬가지로 믹스인의 메소드.
        messages.error(self.request, "호스트가 아닙니다.")
        return redirect(reverse("core:home"))


class PhotoHostOnlyView(UserPassesTestMixin):

    """ Check Photo's host for edit room """

    def test_func(self):

        host = self.get_object()
        print(host)
        if self.request.user == host:
            return True
        else:
            return False

    def handle_no_permission(self):
        # 마찬가지로 믹스인의 메소드.
        messages.error(self.request, "호스트가 아닙니다.")
        return redirect(reverse("core:home"))
