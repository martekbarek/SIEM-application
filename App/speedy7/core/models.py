from django.db import models


class Log(models.Model):
    datetime = models.DateTimeField()
    facility = models.CharField(max_length=20)
    level = models.CharField(max_length=20)
    host = models.CharField(max_length=32)
    program = models.CharField(max_length=20)
    pid = models.CharField(max_length=8)
    message = models.CharField(max_length=255)
    