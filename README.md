django-googleauth
=================

Install
```
pip install -e git+git://github.com/sdfsdhgjkbmnmxc/django-googleauth.git#egg=googleauth
```

Setup settings.py
```python
root = os.path.realpath(os.path.dirname(__file__))

MIDDLEWARE_CLASSES = (
    # ....
    'googleauth.middleware.AuthenticationMiddleware',
)

INSTALLED_APPS = (
    # ....
    'googleauth',
)

# get client_secrets.json from http://code.google.com/apis/console
GOOGLEAUTH_CLIENT_SECRETS_FILE = os.path.join(root, 'client_secrets.json')
#GOOGLEAUTH_MODEL = 'myapp.models.MyUser'
GOOGLEAUTH_USERNAME_IN_REQUEST = 'googleauth_user'
GOOGLEAUTH_START_PAGE = '/profile/'
GOOGLEAUTH_LOGIN_PAGE = '/login/'

```

Setup models.py
```python
import googleauth

class MyUser(googleauth.User):
    pass

```

Setup urls.py
```python

urlpatterns = patterns(
    '',
    url(r'^googleauth/', include('googleauth.urls')),
    # ...
)

```

Usage in views.py
```python
from django.conf import settings
import googleauth


@googleauth.required
def mypage(request):
    return HttpResponse('Welcome, {}!'.format(request.myuser)


def index(request):
    if not request.myuser:
        return HttpResponseRedirect(settings.GOOGLEAUTH_LOGIN_PAGE)
    return render(request, 'index.html')

```

Usage in index.html
```html
<form method="post" action="{% url googleauth_login %}">
    {% csrf_token %}
    <input type="submit" value="Login via Google">
</form>

{#  <a href="{% url googleauth_logout %}">logout</a> #}
```
