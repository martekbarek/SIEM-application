from django.db import models

    
class Log(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    facility = models.CharField(max_length=20, blank=True, null=True)
    level = models.CharField(max_length=20, blank=True, null=True)
    host = models.CharField(max_length=32, blank=True, null=True)
    program = models.CharField(max_length=20, blank=True, null=True)
    pid = models.CharField(max_length=8, blank=True, null=True)
    message = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log'

    
