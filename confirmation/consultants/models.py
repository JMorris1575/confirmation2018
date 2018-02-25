from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Critique(models.Model):
    path = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return 'Critique on ' + self.path + ' by ' + self.name()

    def name(self):
        return self.user.first_name + ' ' + self.user.last_name


    class Meta():
        ordering = ['date']