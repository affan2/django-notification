from django.db import models

from django.contrib.auth import get_user_model


class Language(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    language = models.CharField("language", max_length=10)
