# -*- coding:utf-8 -*-
from django.conf import settings


MODEL = getattr(settings, 'GOOGLEAUTH_MODEL', None)

assert hasattr(settings, 'GOOGLEAUTH_CLIENT_SECRETS_FILE'), \
    "settings.GOOGLEAUTH_CLIENT_SECRETS_FILE required " \
    "(json from http://code.google.com/apis/console)"
SECRETS_FILE = settings.GOOGLEAUTH_CLIENT_SECRETS_FILE

TEMP_USER_SESSION_ID = 'googleauth_temp_user_id'
USER_SESSION_ID = 'googleauth_user_id'

REQUEST_ATTR = getattr(settings, 'GOOGLEAUTH_USERNAME_IN_REQUEST',
                      'googleauth_user')
START_PAGE = getattr(settings, 'GOOGLEAUTH_START_PAGE', '/')
LOGIN_PAGE = getattr(settings, 'GOOGLEAUTH_LOGIN_PAGE', '/')
