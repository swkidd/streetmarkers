from django.db import models
from django.contrib.auth.models import User

class Palace(models.Model):
    title = models.CharField(max_length=30)
    createdBy = models.ForeignKey(User, on_delete=models.PROTECT)
    def __str__(self):
        return self.title

class PathType(models.Model):
    typeName = models.CharField(max_length=30)
    def __str__(self):
        return self.typeName

class Path(models.Model):
    title = models.CharField(max_length=30)
    palace = models.ForeignKey(Palace, on_delete=models.PROTECT)
    type = models.ForeignKey(PathType, on_delete=models.PROTECT, null=True)
    def __str__(self):
        return self.title

class MarkerType(models.Model):
    typeName = models.CharField(max_length=30)
    def __str__(self):
        return self.typeName

class Marker(models.Model):
    title = models.CharField(max_length=30)
    infoText = models.TextField()
    lat = models.FloatField()
    lng = models.FloatField()
    path = models.ForeignKey(Path, on_delete=models.PROTECT, null=True)
    type = models.ForeignKey(MarkerType, on_delete=models.PROTECT, null=True)
    def __str__(self):
        return self.title

class PalaceOwner(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    palace = models.ForeignKey(Palace, on_delete=models.CASCADE)
