from django.db import models
from django.conf import settings
from activity.models import Activity

# Create your models here.


class DevelopingActivity(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    initiator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=15,
                              choices=[('DV', 'Developing'),
                                       ('RV', 'Reviewing'),
                                       ('RD', 'Ready'),
                                       ('PB', 'Published')])

    def __str__(self):
        return self.activity.name

    class Meta:
        verbose_name_plural = 'developing activities'


class Developer(models.Model):
    activity = models.ForeignKey(DevelopingActivity, on_delete=models.CASCADE)
    partner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_partner = models.BooleanField(default=False)

    def __str__(self):
        return self.initiator.first_name + ' ' + self.initiator.last_name + ': ' + activity.name


class Comment(models.Model):
    activity = models.ForeignKey(DevelopingActivity, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    type = models.CharField(max_length=15, choices = [('GN', 'General'),
                                                      ('PT', 'Partners Only')])

    def __str__(self):
        return 'Comment by ' + self.user.first_name + ' ' + self.user.last_name
    