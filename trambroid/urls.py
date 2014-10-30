from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from apps.core.widgy_site import site as widgy_site

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'apps.core.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'mezzanine.pages.views.page', {'slug': '/'}, name='home'),

    url(r'^admin/', include(admin.site.urls)),

    # widgy admin
    url(r'^admin/widgy/', include(widgy_site.urls)),
    # widgy frontend
    url(r'^widgy/', include('widgy.contrib.widgy_mezzanine.urls')),
    url(r'^', include('mezzanine.urls')),
)
