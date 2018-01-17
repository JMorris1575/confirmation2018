from django.db import models

# Create your models here.

class Activity(models.Model):
    index = models.PositiveSmallIntegerField(unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=20, unique=True)
    overview = models.CharField(max_length=512, blank=True)
    publish_date = models.DateField()
    closing_date = models.DateField()
    visible = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['index']


class Page(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE())
    index = models.PositiveSmallIntegerField()
    page_type = models.CharField(max_length=20,
                                 choices=[('ES', 'Essay'),
                                          ('MC', 'MultipleChoice'),
                                          ('TF', 'True-False'),
                                          ('DS', 'Discussion')])
    text = models.CharField(max_length=512)
    explanation = models.CharField(max_length=512, blank=True)
    opinion = models.BooleanField(default=False)        # opinion questions do not have right and wrong answers
    reveal_answer = models.BooleanField(blank=True)     # indicates whether the answer is revealed after user's response
    visible = models.BooleanField(default=True)         # indicates whether the page will be visible
    tf_answer = models.BooleanField(blank=True)         # correct response to True/False questions if opinion=False
    open = models.BooleanField(default=True)            # indicates whether a discussion or poll is open or anonymous

    class Meta:
        unique_together = ('activity', 'index')
        ordering = ['activity', 'index']

    def __str__(self):
        return str(self.activity) + ' - Page ' + str(self.index)

    def get_absolute_url(self):
        return '/activity/' + self.activity.slug + '/' + str(self.index) + '/'

    def previous(self):
        # how do I make sure this doesn't lead the user to improper places or make sure it
        # goes to display rather than input pages?
        index = self.index
        slug = self.activity.slug
        if index == 1:
            return '/activity/' + slug + '/'
        else:
            return '/activity/' + slug + '/' + str(index - 1) + '/'

    def next(self):
        # how do I make sure this doesn't lead the user to a page he or she is not allowed
        # to visit yet?
        index = self.index
        slug = self.activity.slug
        max = len(Page.objects.filter(activity=self.activity))
        if index == max:
            return '/activity/' + slug + '/congrats/'
        else:
            return '/activity/' + slug + '/' + str(index + 1) + '/'