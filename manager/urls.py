from django.conf.urls import url,include
from manager import views

urlpatterns = [
	url(r'^$',views.home),
	url(r'^signin/$',views.signin,name='signin'),
	url(r'^signin_auth/$',views.signin_auth,name='signin_auth'),
	url(r'^assignreviewer/$', views.assign_reviewer),
	url(r'^conference_landing/(?P<cid>[0-9]+)/(?P<type>[0-9])/$',views.conference_landing,name='conference_landing'),
]