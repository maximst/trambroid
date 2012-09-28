from django.conf.urls import patterns, include, url

from django.contrib import admin

from content.views import blog_list, blog_detail

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'trambroid.views.home', name='home'),
    # url(r'^trambroid/', include('trambroid.foo.urls')),
    url(r'^blog/(?P<slug>[\w\-]+)/$', blog_detail, name='blog'),
    url(r'^blog/$', blog_list, name='blog-list'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^comments/', include('django.contrib.comments.urls')),
)
