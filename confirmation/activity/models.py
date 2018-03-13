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
    publish_date = models.DateField(null=True)
    closing_date = models.DateField(null=True)
    visible = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['index']
        verbose_name_plural = 'activities'


class Page(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    index = models.PositiveSmallIntegerField()
    page_type = models.CharField(max_length=20,
                                 choices=[('IN', 'Instructions'),
                                          ('ES', 'Essay'),
                                          ('MC', 'MultipleChoice'),
                                          ('TF', 'True-False'),
                                          ('DS', 'Discussion'),
                                          ('CH', 'Challenge')])
    title = models.CharField(max_length=40)
    text = models.CharField(max_length=512)
    image = models.ForeignKey(Image, null=True, blank=True, on_delete=models.CASCADE)
    explanation = models.CharField(max_length=512, blank=True)
    timed = models.BooleanField(default=False)          # indicates whether this page is timed
    opinion = models.BooleanField(default=False)        # opinion questions do not have right and wrong answers
    reveal_answer = models.BooleanField(blank=True)     # indicates whether the answer is revealed after user's response
    visible = models.BooleanField(default=True)         # indicates whether the page will be visible
    tf_answer = models.BooleanField(blank=True)         # correct response to True/False questions if opinion=False
    discussion_type = models.CharField(max_length=20,   # indicates type of discussion
                                       choices=[('OP', 'Open'),
                                                ('SA', 'Semi-Anonymous'),
                                                ('AN', 'Anonymous')],
                                       blank=True,
                                       default='')

    class Meta:
        unique_together = ('activity', 'index')
        ordering = ['activity', 'index']

    def __str__(self):
        return self.activity.slug + ': ' + str(self.index) + '. ' + str(self.title)

    def get_absolute_url(self):
        return '/activity/' + self.activity.slug + '/' + str(self.index) + '/'

    def allowed(self, user, activity_slug, page_index):
        """
        Returns True if the user is allowed to go to the page at /activity/<activity_slug>/<page_index>, having
        completed the page just before this one
        :return: boolean
        """
        if self.index == 1:
            return True             # user is always allowed to go to the first page
        else:
            activity = Activity.objects.get(slug=activity_slug)
            pages = Page.objects.filter(activity=activity)
            result = True
            for page in pages:
                if page.index < page_index:
                    responses = Response.objects.filter(user=user, activity=activity, page=page)
                    if len(responses) == 0:
                        result = False
                        break
            return result

    def previous(self):
        """
        Returns the previous page if there is one, otherwise returns None
        :return: '/activity/<activity_slug>/<page_index>/ or None
        """
        index = self.index
        slug = self.activity.slug
        if index == 1:
            return None
        else:
            return '/activity/' + slug + '/' + str(index - 1) + '/'

    def next(self):
        """
        Returns the next page if there is one, otherwise returns None
        :return: '/activity/<activity_slug>/<page_index>/ or None
        """
        index = self.index
        slug = self.activity.slug
        max = len(Page.objects.filter(activity=self.activity))
        if index == max:
            return None
        else:
            return '/activity/' + slug + '/' + str(index + 1) + '/'

    def discussion_explanation(self):
        if self.discussion_type == 'OP':
            msg = "In an open discussion, your name will appear next to each entry you make and you will be able to "
            msg += "edit your entries at any time."
        elif self.discussion_type == 'SA':
            msg = "In a semi-anonymous discussion, your name will NOT appear next to your entries but team members "
            msg += "be able to see who made each comment. You will be able to edit your entries at any time."
        else:
            msg = "In an anonymous discussion your name is not recorded anywhere in the system and no one will be able "
            msg += "to tell who made which comment and edits will not be possible. Keep in mind, however, nothing on "
            msg += "the internet is completely anonymous."
        return msg


class Response(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
    essay = models.TextField(blank=True)
    multi_choice = models.PositiveSmallIntegerField(null=True, blank=True)
    true_false = models.BooleanField(default=False)
    correct = models.NullBooleanField(null=True)
    completed = models.BooleanField(default=False)

    class Meta():
        ordering = ['created']

    def __str__(self):
        name = self.user.first_name + ' ' + self.user.last_name
        if name[-1] == 's':
            possessive_ending = "'"
        else:
            possessive_ending = "'s"
        return name + possessive_ending + ' response to ' + str(self.page)

    def is_correct(self):
        return self.correct

    def can_delete(self):
        """
        Returns True if this response can be deleted, false otherwise
        A response can be deleted if it's answer has not been revealed and if the user has not completed any pages
        beyond this one in the current activity
        :return: boolean
        """
        this_index = self.page.index
        number_completed = len(Response.objects.filter(user=self.user, activity=self.activity))
        if (this_index == number_completed) and not self.page.reveal_answer:
            return True
        else:
            return False

    def can_goto_next(self):
        """
        Returns true if this user has completed this page and so can go to the next
        :return: boolean
        """
        return self.completed

    def user_choice(self):
        return Choice.objects.get(page=self.page, index=int(self.multi_choice))

class Choice(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    index = models.PositiveSmallIntegerField()
    text = models.CharField(max_length = 256)
    correct = models.BooleanField(blank=True)       # indicates this choice is correct if opinion is False in Page model

    def __str__(self):
        return self.choiceLetter(self.index) + self.text

    def choiceLetter(self, index):
        return chr(64 + index) + ') '

    def correct_choice(self):
        return Choice.objects.get(page=self.page, correct=True)


    class Meta:
        ordering = ['page', 'index']


