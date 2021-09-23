from django.conf.urls import url

from .views import (vote, logout, registration,
                    registration_thanks, set_language)

urlpatterns = [
    url(r'^vote/(?P<app>[\w\-\_]+)/(?P<model>[\w\_]+)/(?P<pk>\d+)/(?P<vote>(-?[01]))/$', vote, name='vote'),
    url(r'^logout/$', logout, name='logout'),
    #url(r'^accounts/registration/$', registration, name='registration'),
    #url(r'^accounts/registration_thanks/$', registration_thanks,
    #                                        name='registration-thanks'),
    url(r'^language/(?P<lang>[a-z]{2})', set_language, name='set-language'),
]
