from django.conf.urls import patterns, url
import views


urlpatterns = patterns(
    '',
    url(r'^login/$', views.login, name='googleauth_login'),
    url(r'^callback/$', views.oauth2callback),
    url(r'^logout/$', views.logout, name='googleauth_logout'),
)
