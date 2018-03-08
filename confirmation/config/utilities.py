from django.contrib.auth.models import Group, User, AnonymousUser
from activity.models import Activity, Page, Response
from consultants.models import Critique


def get_group_names(user):
    """
    returns a list of all the names of the groups to which user belongs
    :param user: instance of the User model, probably from request.user
    :return: a list of strings, the names of the groups to which this user belongs
    """
    group_names = []
    if not(user.is_anonymous):
        for group in Group.objects.filter(user=user):
            group_names.append(group.name)
    return group_names

def get_response_info(user=None, activity_slug=None, page_index=None):
    activity = Activity.objects.get(slug=activity_slug)
    page = Page.objects.get(activity=activity, index=page_index)
    responses = Response.objects.filter(user=user, activity=activity, page=page)
    response = None              # single_response = None for no responses and if there are more than one
    if len(responses) == 1:
        response = responses[0]
    context = {'activity':activity, 'page':page, 'response':response, 'group_names':get_group_names(user)}
    return activity, page, responses, context

def is_candidate(user):
    groups = get_group_names(user)
    return 'Candidate' in groups

def is_tester(user):
    groups = get_group_names(user)
    return 'Tester' in groups

def get_critiques(path):
    return Critique.objects.filter(path=path)

def get_welcome_report():
    """
    Gets the candidate report for the welcome page as to which activities the user has so far participated in.
    :return: an ordered list of tuples ordered by last_name, first_name with the user's full name in position 0
            and a string of the activities in which they have so far participated in position 1.
    """
    users = User.objects.all().order_by('last_name', 'first_name')
    activities = Activity.objects.all()
    report = []
    for user in users:
        if is_candidate(user):
            if user.first_name != 'Unknown':
                user_name = user.last_name + ', ' + user.first_name
                activity_list = ''
                for activity in activities:
                    if len(Response.objects.filter(user=user, activity=activity)) != 0:
                        if len(activity_list) == 0:
                            activity_list += str(activity.slug)
                            print('activity_list = ', activity_list)
                        else:
                            activity_list += ', ' + str(activity.slug)
                report.append((user_name, activity_list))
    return report


class PageMixin:

    """
    This mixin gets a response or QuerySet of responses with the corresponding activity and page
    from the user, activity_slug and page_index

    The methods simply wrap the routines above so that the routines above can be used as utilities
    """

    def get_group_names(self, user):
        return get_group_names(user)

    def get_response_info(self, user=None, activity_slug=None, page_index=None):
        return get_response_info(user, activity_slug, page_index)