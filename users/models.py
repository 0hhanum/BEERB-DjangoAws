from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


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

    avatar = models.ImageField(blank=True)  # 데이터베이스의 값이 null 이어도 허용
    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=10, blank=True
    )  # blank 이용 필수입력항목 해제
    bio = models.TextField(blank=True)  # 데이터베이스 기본값을 "" 로 설정
    # CharField 는 한줄, 글자수 제한. TextField 는 자유.
    birthdate = models.DateField(blank=True, null=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=2, blank=True)
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3, blank=True)
    superhost = models.BooleanField(default=False)
