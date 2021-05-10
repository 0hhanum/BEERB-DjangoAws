import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string


class User(AbstractUser):

    """ Custom User Model """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),  # GENDER_MALE 이 admin 패널로 전송, Male 이 Form 에 보여진다.
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "ko"

    LANGUAGE_CHOICES = (
        (LANGUAGE_KOREAN, "Korean"),
        (LANGUAGE_ENGLISH, "English"),
    )

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = ((CURRENCY_KRW, "KRW"), (CURRENCY_USD, "USD"))

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_KAKAO = "kakao"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GITHUB, "Github"),
        (LOGIN_KAKAO, "Kakao"),
    )

    avatar = models.ImageField(
        blank=True, upload_to="avatars"
    )  # 데이터베이스의 값이 null 이어도 허용
    # media root 안의 어떤 폴더에 저장할 건지 설정.
    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=10, blank=True
    )  # blank 이용 필수입력항목 해제
    bio = models.TextField(blank=True)  # 데이터베이스 기본값을 "" 로 설정
    # CharField 는 한줄, 글자수 제한. TextField 는 자유.
    birthdate = models.DateField(blank=True, null=True)
    language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=2, blank=True, default=LANGUAGE_KOREAN
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3, blank=True, default=CURRENCY_KRW
    )
    superhost = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=120, default="", blank=True)
    login_method = models.CharField(
        max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )

    # def verify_email(self):
    #     if self.email_verified is False:
    #         secret = uuid.uuid4().hex[:20]
    #         self.email_secret = secret
    #         html_message = render_to_string(
    #             "emails/verify_email.html", {"secret": secret}
    #         )
    #         send_mail(
    #             " 본인을 확인해주세요. ",
    #             strip_tags(html_message),
    #             settings.EMAIL_FROM,
    #             [self.email],
    #             fail_silently=False,
    #             html_message=html_message,
    #         )
    #     self.save()
    #     return
