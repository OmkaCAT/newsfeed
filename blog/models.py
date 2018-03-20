from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    published_date = models.DateTimeField(
            default=timezone.now)

    def __str__(self):
        return self.title


class Captcha(models.Model):
    captcha = models.CharField(max_length=200)
    token = models.CharField(max_length=200)
