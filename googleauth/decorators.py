# -*- coding:utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from conf import REQUEST_ATTR
from views import login


def required(func):
    def decorated(request, *args, **kwargs):
        user = getattr(request, REQUEST_ATTR)
        if not user:
            return HttpResponseRedirect(reverse(login))
        return func(request, *args, **kwargs)
    return decorated

