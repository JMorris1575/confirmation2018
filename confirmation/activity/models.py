from django.db import models
from django.conf import settings

# Create your models here.

class Image(models.Model):
    filename = models.CharField(max_length=30)
    category = models.CharField(max_length=20)

    def __str__(self):
        return self.filename


class Activity(models.Model):
    index = models.PositiveSmallIntegerField(unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=20, unique=True)
    overview = models.CharField(max_length=512, blank=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, blank=True)
    publish_date = models.DateField()
    closing_date = models.DateField()
    visible = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['index']


class Page(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    index = models.PositiveSmallIntegerField()
    page_type = models.CharField(max_length=20,
                                 choices=[('IN', 'Instructions'),
                                          ('ES', 'Essay'),
                                          ('MC', 'MultipleChoice'),
                                          ('TF', 'True-False'),
                                          ('DS', 'Discussion')])
    title = models.CharField(max_length=25)
    text = models.CharField(max_length=512)
    image = models.ForeignKey(Image, null=True, blank=True, on_delete=models.CASCADE)
    explanation = models.CharField(max_length=512, blank=True)
    timed = models.BooleanField(default=False)          # indicates whether this page is timed
    opinion = models.BooleanField(default=False)        # opinion questions do not have right and wrong answers
    reveal_answer = models.BooleanField(blank=True)     # indicates whether the answer is revealed after user's response
    visible = models.BooleanField(default=True)         # indicates whether the page will be visible
    tf_answer = models.BooleanField(blank=True)         # correct response to True/False questions if opinion=False
    open = models.BooleanField(default=True)            # indicates whether a discussion or poll is open or anonymous

    class Meta:
        unique_together = ('activity', 'index')
        ordering = ['activity', 'index']

    def __str__(self):
        return str(self.index) + '. ' + str(self.title)

    def get_absolute_url(self):
        return '/activity/' + self.activity.slug + '/' + str(self.index) + '/'

    def previous(self):
        # how do I make sure this doesn't lead the user to improper places or make sure it
        # goes to display rather than input pages?
        index = self.index
        slug = self.activity.slug
        if index == 1:
            return None
        else:
            return '/activity/' + slug + '/' + str(index - 1) + '/'

    def next(self):
        # how do I make sure this doesn't lead the user to a page he or she is not allowed
        # to visit yet?
        index = self.index
        slug = self.activity.slug
        max = len(Page.objects.filter(activity=self.activity))
        if index == max:
            return None
        else:
            return '/activity/' + slug + '/' + str(index + 1) + '/'


class Response(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
    essay = models.TextField(blank=True)
    multi_choice = models.CharField(max_length=1, blank=True)
    true_false = models.NullBooleanField()
    correct = models.NullBooleanField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        name = self.user.first_name + ' ' + self.user.last_name
        if name[-1] == 's':
            possessive_ending = "'"
        else:
            possessive_ending = "'s"
        return name + possessive_ending + ' response to ' + str(self.activity) + ' ' + str(self.page)


class Choice(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    index = models.PositiveSmallIntegerField()
    text = models.CharField(max_length = 256)
    correct = models.BooleanField(blank=True)       # indicates this choice is correct if opinion if False in Page model

    def __str__(self):
        return self.choiceLetter(self.index) + self.text

    def choiceLetter(self, index):
        return chr(64 + index) + ') '


