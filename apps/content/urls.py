from django.conf.urls import url

from .views import blog_list, blog_detail, tags


urlpatterns = [
    url(r'^blog/(?P<slug>[\w\-]+)/$', blog_detail, name='detail'),
    url(r'^blog/$', blog_list, name='list'),

    # Drupal URLs
    url(r'^(?:(?P<lang>ru|en)/)?node/(?P<slug>\d+)/$', blog_detail, {'is_drupal': True}),
    url(r'^(?:(?P<lang>ru|en)/)?(?P<slug>(?:contents?|nodes?|news_nix)\/[^/]+)/$', blog_detail, {'is_drupal': True}),
    url(r'^(?:(?P<lang>ru|en)/)?(?:poll|news_nix|content|blogs?|nodes?)/$', blog_list),
    url(r'^(?:(?P<lang>ru|en)/(?:node/)?|node/)$', blog_list),
    url(r'^(?:(?P<lang>ru|en)/)?(?P<drupal_blogs_alias_url>blogs/.+)/$', blog_list),
#    url(r'^(?:(?P<lang>ru|en)/)?blog/(?P<drupal_uid>\d+)/$', blog_list),

    url(r'^tags?/(?P<tag>.+)/$', tags, name='tag'),
    url(r'^tags?/$', tags, name='tag-list'),

    url(r'^(?:ru/|en/)?tags/(?:(?P<tag>.+)/)?$', tags),
]
