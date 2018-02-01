from activity.models import Activity, Page, Response

class ResponseMixin:

    """
    This mixin gets single responses from the Response model depending on the user, activity and page
    """

    def get_response_info(self, user=None, activity_slug=None, page_index=None):
        activity = Activity.objects.get(slug=activity_slug)
        page = Page.objects.get(activity=activity, index=page_index)
        try:
            response = Response.objects.get(user=user, activity=activity, page=page)
        except Response.DoesNotExist:
            response = None
        return activity, page, response


