from django.conf.urls import url

from blacklist_check import view

urlpatterns = [
    url(r'^index$', view.index, name='index'),
    url(r'^view/(?P<pk>[0-9]+)$', view.ip, name='ip'),
]
