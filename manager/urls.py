from django.conf.urls import url,include
from manager import views

urlpatterns = [
	url(r'^assignreviewer/(?P<paper_id>[A-Za-z0-9.-]+)/$', views.assign_reviewer),
	url(r'^reviewcomplete/(?P<paper_id>[A-Za-z0-9.-]+)/(?P<u_id>[A-Za-z0-9.-]+)/$', views.reviewCompleted),
	url(r'^$',views.home),
	url(r'^signin/$',views.signin,name='signin'),
	url(r'^signin_auth/$',views.signin_auth,name='signin_auth'),
	url(r'^assignreviewer/', views.assign_reviewer),
]