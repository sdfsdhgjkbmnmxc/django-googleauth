# -*- coding:utf-8 -*-
from django.utils.importlib import import_module
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings


TEMP_USER_SESSION_ID = 'googleauth_temp_user_id'
USER_SESSION_ID = 'googleauth_user_id'


def get_model():
    module, attr = settings.GOOGLEAUTH_MODEL.rsplit('.', 1)
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured('Error importing module %s: "%s"' %
                                   (module, e))
    try:
        Model = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a "%s" '
                                   'class.' % (module, attr))
    return Model


def required(func):
    def decorated(request, *args, **kwargs):
        user_id = request.session.get(USER_SESSION_ID)
        try:
            request.doer = get_model().objects.get(id=user_id)
        except:
            return HttpResponseRedirect(reverse(login))
        else:
            return func(request, *args, **kwargs)
    return decorated
