"""trambroid URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from django.views import static
import supercaptcha

from apps.content.views import blog_list
from apps.core.views import vote, logout, profile


urlpatterns = [
    url(r'^$', blog_list, name='home'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    path('admin/', admin.site.urls),

    path('', include(('apps.content.urls', 'content'), namespace='content')),

    path('', include(('apps.core.urls', 'core'), namespace='core')),

    path('', include(('apps.user_profile.urls', 'user_profile'), namespace='profile')),

    path('', include(('apps.drupal.urls', 'drupal'), namespace='forum')),

    path('', include(('social.apps.django_app.urls', 'django_app'), namespace='social')),

    url(r'^captcha/(?P<code>[\da-f]{32})/$', supercaptcha.draw),
]

if settings.DEBUG:
    urlpatterns.append(url(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}))
