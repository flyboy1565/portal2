from django.db import models


from .locations.models import Store


class PhoneTags(models.Model):
    tag = models.CharField(max_length=5)
    description = models.CharField(max_length=50)
    
    def __str__(self):
        return self.tag


class PhoneLine(models.Model):
    
