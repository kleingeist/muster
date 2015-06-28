from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/muster/'}),
    url(r'^$', views.index, name='index'),
    url(r'^volume/(?P<volume_rid>[\w\.\-]+)$',
        views.volume_detail, name="volume_detail"),
    url(r'^page/(?P<page_rid>[\w\.\-]+)$',
        views.page_browser, name="page_browser"),
    url(r'^search$', views.search, name="search"),
    url(r'^pattern/(?P<pattern_id>[0-9]+)/(?P<vector_id>[0-9]+)$',
        views.pattern_detail, name="pattern_detail"),
    url(r'^add_tag/(?P<pattern_id>[0-9]+)$', views.add_tag, name="add_tag"),
    url(r'^rate_vector/(?P<vector_id>[0-9]+)$', views.rate_vector, name="rate_vector"),
]
