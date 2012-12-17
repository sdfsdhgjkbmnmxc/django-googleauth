# -*- coding:utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.utils import simplejson
from googleauth.core import TEMP_USER_SESSION_ID, get_model, USER_SESSION_ID
from oauth2client import xsrfutil
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import httplib2
import random
import sys


def oauth2callback(request):
    t = request.session.get(TEMP_USER_SESSION_ID)
    if not t:
        return HttpResponseRedirect(reverse(login))

    state = request.REQUEST['state']
    if not xsrfutil.validate_token(settings.SECRET_KEY, state, t):
        return HttpResponseBadRequest()

    try:
        credential = _get_flow(request).step2_exchange(request.REQUEST)
    except FlowExchangeError:
        return HttpResponseRedirect(reverse(login))

    if credential.invalid:
        return HttpResponseRedirect(reverse(login))

    http = httplib2.Http()
    http = credential.authorize(http)
    _h, c = http.request('https://www.googleapis.com/oauth2/v1/userinfo')
    data = simplejson.loads(c)
    doer, _created = get_model().objects.get_or_create(
        email=data['email'],
        defaults=dict(
            name=data.get('name') or data['email'].split('@')[0],
        )
    )
    doer.name = data.get('given_name') or doer.name
    doer.surname = data.get('family_name', '')
    doer.save()

    request.session['doer_id'] = doer.id
    return HttpResponseRedirect('/')


def login(request):
    if TEMP_USER_SESSION_ID in request.session:
        request.session[TEMP_USER_SESSION_ID] = None
    if request.session.get(USER_SESSION_ID):
        return HttpResponseRedirect('/')
    elif request.method == 'POST':
        t = random.randint(0, sys.maxint)
        flow = _get_flow(request)
        flow.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, t)
        request.session[TEMP_USER_SESSION_ID] = t
        return HttpResponseRedirect(flow.step1_get_authorize_url())
    else:
        return render(request, 'login.html', {})


def logout(request):
    if USER_SESSION_ID in request.session:
        del request.session[USER_SESSION_ID]
    return HttpResponseRedirect(reverse(login))


def _get_flow(request):
    # http://code.google.com/apis/console
    return flow_from_clientsecrets(
        settings.GOOGLEAUTH_CLIENT_SECRETS_FILE,
        scope=[
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile',
        ],
        redirect_uri=request.build_absolute_uri(reverse(oauth2callback)),
    )
