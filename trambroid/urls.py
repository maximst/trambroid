from django.conf.urls import patterns, include, url

from django.contrib import admin

from content.views import blog_list, blog_detail
from core.views import vote

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^blog/(?P<slug>[\w\-]+)/$', blog_detail, name='blog'),
    url(r'^blog/(\?p=\d+)?$', blog_list, name='blog-list'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^vote/(?P<app>[\w\-\_]+)/(?P<model>[\w\_]+)/(?P<pk>\d+)/(?P<vote>(-?[01]))/$', vote, name='vote'),
)
