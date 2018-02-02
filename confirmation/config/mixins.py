from activity.models import Activity, Page, Response

class ResponseMixin:

    """
    This mixin gets a response or QuerySet of responses with the corresponding activity and page
    from the user, activity_slug and page_index
    """

    def get_response_info(self, user=None, activity_slug=None, page_index=None):
        activity = Activity.objects.get(slug=activity_slug)
        page = Page.objects.get(activity=activity, index=page_index)
        responses = Response.objects.filter(user=user, activity=activity, page=page)
        single_response = None              # single_response = None for no responses and if there are more than one
        if len(responses) == 1:
            response = responses[0]
        context = {'activity':activity, 'page':page, 'response':single_response}
        return activity, page, responses, context


