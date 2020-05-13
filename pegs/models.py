from django.db import models
from django.contrib.auth.models import User

class PegSystem(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    createdBy = models.ForeignKey(User, on_delete=models.PROTECT)
    
    @property
    def peg_count(self):
        return len(self.peg_set)

    def __str__(self):
        return self.title

class PegType(models.Model):
    typeName = models.CharField(max_length=30)
    def __str__(self):
        return self.typeName

class Peg(models.Model):
    content = models.CharField(max_length=30)
    notes = models.TextField(null=True, blank=True)
    pegSystem = models.ForeignKey(PegSystem, on_delete=models.CASCADE)
    pegType = models.ForeignKey(PegType, on_delete=models.PROTECT, null=True)
    def __str__(self):
        return self.content

class BasicPeg(Peg):
    encoded = models.CharField(max_length=30)

class PAOPeg(Peg): 
    person = models.CharField(max_length=30)
    action = models.CharField(max_length=30)
    object = models.CharField(max_length=30)

class POPeg(Peg): 
    person = models.CharField(max_length=30)
    object = models.CharField(max_length=30)