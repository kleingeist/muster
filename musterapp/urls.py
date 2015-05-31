from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^page/(?P<page_rid>[\w\.\-]+)$',
        views.page_browser, name="page_browser"),
]
