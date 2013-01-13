# -*- coding:utf-8 -*-
from urllib import urlencode

from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect

from googleauth.conf import USER_SESSION_ID, REQUEST_ATTR, LOGIN_PAGE
from googleauth.models import get_model


class AuthenticationMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session'), "session middleware required"
        user = _get_user_or_none(request)
        if user:
            try:
                user.clean()
            except ValidationError, e:
                del request.session[USER_SESSION_ID]
                return redirect_to_login_page(e.messages[0])
        setattr(request, REQUEST_ATTR, user)


def _get_user_or_none(request):
    user_id = request.session.get(USER_SESSION_ID)
    Model = get_model()
    try:
        return Model.objects.get(id=user_id)
    except Model.DoesNotExist:
        return None


def redirect_to_login_page(reason=None):
    url = LOGIN_PAGE
    if reason:
        sep = '&' if ('?' in url) else '?'
        url += sep + urlencode({'reason': reason})
    return HttpResponseRedirect(url)
