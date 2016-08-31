from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<conferenceAlias>.+)/(?P<subpage>.+)/$', views.subpage),
    url(r'^(?P<conferenceAlias>.+)/$', views.home),
    

    url(r'^$', views.index, name='index'),
]
