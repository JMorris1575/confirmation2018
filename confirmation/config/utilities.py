from django.contrib.auth.models import Group
from activity.models import Activity, Page, Response


def get_group_names(user):
    """
    returns a list of all the names of the groups to which user belongs
    :param user: instance of the User model, probably from request.user
    :return: a list of strings, the names of the groups to which this user belongs
    """
    group_names = []
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