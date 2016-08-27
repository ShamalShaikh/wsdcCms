from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<conferenceName>.+)/(?P<subpage>.+)/$', views.subpage),
    url(r'^(?P<conferenceName>.+)/$', views.home),

    url(r'^$', views.index, name='index'),
]
