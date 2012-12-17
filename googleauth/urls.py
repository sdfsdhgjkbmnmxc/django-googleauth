from django.conf.urls import patterns, url
import views


urlpatterns = patterns(
    '',
    url(r'^$', views.login, name='login'),
    url(r'^oauth2callback/$', views.oauth2callback, name='oauth2callback'),
    url(r'^logout/$', views.logout, name='logout'),
)
