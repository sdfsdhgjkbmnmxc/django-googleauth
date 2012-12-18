# -*- coding:utf-8 -*-
from core import required
from models import User
from django.conf import settings


assert hasattr(settings, 'GOOGLEAUTH_MODEL'), \
    "settings.GOOGLEAUTH_MODEL = 'path.to.Model' required"

assert hasattr(settings, 'GOOGLEAUTH_CLIENT_SECRETS_FILE'), \
    "settings.GOOGLEAUTH_CLIENT_SECRETS_FILE required " \
    "(json from http://code.google.com/apis/console)"
