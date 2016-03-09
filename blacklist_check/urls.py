from django.conf.urls import patterns, url

from blacklist_check import view
urlpatterns = patterns(
    '',
    url(r'^index/$', view.index, name='index'),
    url(r'^view/(?P<pk>[0-9]+)$', view.ip, name='cryptocoin-order-check-status'),
)
