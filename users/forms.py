from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    # def clean_email(self):

    #     email = self.cleaned_data.get("email")
    #     try:
    #         models.User.objects.get(username=email)
    #         return email

    #     except models.User.DoesNotExist:
    #         raise forms.ValidationError("User does not exist")

    #     return "la"

    # def clean_password(self):

    #     email = self.cleaned_data.get("email")
    #     password = self.cleaned_data.get("password")

    #     try:
    #         user = models.User.objects.get(username=email)
    #         if user.check_password():
    #             return password

    #         else:
    #             raise forms.ValidationError("Password is wrong")

    #     except models.User.DoesNotExist:

    #         pass

    # 서로 연관된 데이터에 clean 실행할 때는 이런 식으로.
    def clean(self):

        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data

            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))

        except models.User.DoesNotExist:

            raise self.add_error("email", forms.ValidationError("User does not exist"))


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")

    password = forms.CharField(widget=forms.PasswordInput(), label="비밀번호")
    password1 = forms.CharField(widget=forms.PasswordInput(), label="비밀번호 확인")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("이미 존재하는 사용자입니다.")
        except models.User.DoesNotExist:
            # 헷갈리면 안됨. User 가 없으면 Error 발생할것임. 그러면 여기로 넘어오는것.
            return email

    def clean_password1(self):  # password 로 하면 password1 이 clean 되기 전이라 불러올 수 없음.

        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    # ModelForm 의 save 메소드 오버라이드
    def save(self, *args, **kwargs):
        user = super().save(commit=False)  # Object 는 만들어지지만 데이터베이스에 save 는 하지 않음.

        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()


"""
class SignUpForm(forms.Form):

    first_name = forms.CharField(max_length=80)
    last_name = forms.CharField(max_length=80)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("이미 존재하는 사용자입니다.")
        except models.User.DoesNotExist:
            # 헷갈리면 안됨. User 가 없으면 Error 발생할것임. 그러면 여기로 넘어오는것.
            return email

    def clean_password1(self):  # password 로 하면 password1 이 clean 되기 전이라 불러올 수 없음.

        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    def save(self):

        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        user = models.User.objects.create_user(email, email, password)
        # create 와 다르게 User 의 create_user 는 password 를 암호화하여 저장.
        user.first_name = first_name
        user.last_name = last_name
        user.save()
"""
