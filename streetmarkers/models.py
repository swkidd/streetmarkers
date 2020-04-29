from django.db import models

class Marker(models.Model):
    title = models.CharField(max_length=30)
    infoText = models.TextField()
    lat = models.FloatField()
    lng = models.FloatField()
    def __str__(self):
        return self.title