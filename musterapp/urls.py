from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^volume/(?P<volume_rid>[\w\.]+)$', views.volume_list,
        name='volume_list'),
    url(r'^volume/(?P<volume_rid>[\w\.]+)/(?P<page_number>[\d]+)$',
        views.volume_list, name='volume_list_number')
]
