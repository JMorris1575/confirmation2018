from django.db import models

# Create your models here.

class Activity(models.Model):
    index = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    overview = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['index']

