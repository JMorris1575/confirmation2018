from django.db import models

# Create your models here.


class HelpCategory(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta():
        verbose_name_plural = 'help categories'

class HelpPage(models.Model):
    category = models.ForeignKey(HelpCategory, on_delete=models.CASCADE, null=True)
    number = models.SmallIntegerField()
    name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.category) + ": " + str(self.number) + '. ' + self.name

    class Meta():
        unique_together = (("category", "number"))
        ordering = ['category', 'number']