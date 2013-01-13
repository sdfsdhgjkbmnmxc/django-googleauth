# -*- coding:utf-8 -*-
from googleauth.conf import USER_SESSION_ID, REQUEST_ATTR
from googleauth.models import get_model


class AuthenticationMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session'), "session middleware required"
        user = _get_user_or_none(request)
        setattr(request, REQUEST_ATTR, user)


def _get_user_or_none(request):
    user_id = request.session.get(USER_SESSION_ID)
    Model = get_model()
    try:
        return Model.objects.get(id=user_id)
    except Model.DoesNotExist:
        return None
