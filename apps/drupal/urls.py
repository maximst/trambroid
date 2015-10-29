from django.conf.urls import url

from .views import forum


urlpatterns = [
    url(r'^forum/$', forum, name='list'),
    url(r'^(?:en\/|ru\/)?(?P<path>forum[sy]?)/(?:(?P<slug>.+)/)?$', forum),
]
