from django.conf.urls import url

from .views import profile

urlpatterns = [
    url(r'^(?:accounts/)?(profile|user|users)/(?:(?P<username>\w+)/)?$', profile, name='profile', ),
    url(r'^accounts/$', profile),
]
