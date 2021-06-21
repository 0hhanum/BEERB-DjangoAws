from django.db import models
from . import managers

# Create your models here.


class TimeStampedModel(models.Model):

    """ Time Stamped Model """

    created = models.DateTimeField(auto_now_add=True)  # 새로 만들 때 시간 기록
    updated = models.DateTimeField(auto_now=True)  # 매번 시간 기록 (create 와 update 다르게)
    objects = managers.CustomModelManager()

    class Meta:
        abstract = True  # model 이지만 데이터베이스에 나타나지 않게 해줌.
