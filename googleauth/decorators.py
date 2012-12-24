# -*- coding:utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from conf import USER_SESSION_ID, START_PAGE, REQUEST_ATTR
from models import get_model
from views import login


def required(func):
    def decorated(request, *args, **kwargs):
        user = _get_user_or_none(request)
        #print func, 'user', user
        if not user:
            return HttpResponseRedirect(reverse(login))
        setattr(request, REQUEST_ATTR, user)
        return func(request, *args, **kwargs)
    return decorated


def if_logged_in_then_redirect_to_start_page(func):
    def decorated(request, *args, **kwargs):
        user = _get_user_or_none(request)
        if user:
            return HttpResponseRedirect(START_PAGE)
        return func(request, *args, **kwargs)
    return decorated


def _get_user_or_none(request):
    user_id = request.session.get(USER_SESSION_ID)
    #print request.path, 'user_id', user_id
    Model = get_model()
    try:
        return Model.objects.get(id=user_id)
    except Model.DoesNotExist:
        return None
