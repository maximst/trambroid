from django.conf.urls import url

from .views import profile

urlpatterns = [
    url(r'^(profile|user|users)/(?:(?P<username>\w+)/)?$', profile, name='profile', ),
    url(r'^accounts/$', profile),
]