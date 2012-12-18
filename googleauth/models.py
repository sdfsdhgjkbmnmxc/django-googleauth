# -*- coding:utf-8 -*-
import hashlib

from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.importlib import import_module
from django.utils.translation import ugettext_lazy

from conf import MODEL


class User(models.Model):
    GRAVATAR_URL = 'http://www.gravatar.com/avatar/{hash}?d=monsterid'

    creation_datetime = models.DateTimeField(auto_now_add=True)
    name = models.CharField(ugettext_lazy('name'), max_length=255)
    surname = models.CharField(ugettext_lazy('surname'), max_length=255, blank=True)
    email = models.EmailField(ugettext_lazy('email'), unique=True)

    def get_gravatar_url(self):
        s = hashlib.md5(self.email.decode('utf-8')).hexdigest()
        return self.GRAVATAR_URL.format(hash=s)

    def __unicode__(self):
        if self.surname:
            return u'{} {}'.format(self.name, self.surname)
        else:
            return self.name

    def clean(self):
        self.name = self.name.strip()
        self.surname = self.surname.strip()
        self.email = self.email.lower()

    def save(self, *args, **kwargs):
        self.clean()
        super(User, self).save(*args, **kwargs)

    class Meta:
        abstract = True


def get_model():
    module, attr = MODEL.rsplit('.', 1) #@UndefinedVariable
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
