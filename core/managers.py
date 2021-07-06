from django.contrib.auth.models import UserManager
from django.db import models


class CustomModelManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)

        except:
            return None


class CustomUserManager(CustomModelManager, UserManager):
    pass
