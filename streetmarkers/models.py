from django.db import models
from django.contrib.auth.models import User

class Palace(models.Model):
    title = models.CharField(max_length=30)
    createdBy = models.ForeignKey(User, on_delete=models.PROTECT)
    
    def get_user_path_set(self):
        return self.path_set.filter(createdBy=self.createdBy) 
    
    @property
    def path_count(self):
        return len(self.get_user_marker_set())
    
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
    createdBy = models.ForeignKey(User, on_delete=models.PROTECT, null=True)

    def get_user_marker_set(self):
        return self.basemarker_set.filter(path=self)
    
    @property
    def marker_count(self):
        return len(self.get_user_marker_set())


    def __str__(self):
        return self.title

class MarkerType(models.Model):
    typeName = models.CharField(max_length=30)
    def __str__(self):
        return self.typeName

class BaseMarker(models.Model):
    title = models.CharField(max_length=30)
    lat = models.FloatField()
    lng = models.FloatField()
    path = models.ForeignKey(Path, on_delete=models.PROTECT, null=True)
    palace = models.ForeignKey(Palace, on_delete=models.PROTECT, null=True)
    createdBy = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    type = models.ForeignKey(MarkerType, on_delete=models.PROTECT, null=True)
    def __str__(self):
        return self.title

#Maker Type: 'basic'
class BasicMarker(BaseMarker):
    infoText = models.TextField()

class PalaceOwner(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    palace = models.ForeignKey(Palace, on_delete=models.CASCADE)
