from django.db import models

# Create your models here.

class HelpPage(models.Model):
    page = models.SmallIntegerField()
    page_name = models.CharField(max_length=20)

    def __str__(self):
        return self.page_name