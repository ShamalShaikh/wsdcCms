from django.conf.urls import url,include
from . import views

urlpatterns = [
	url(r'^$',views.index),
	url(r'^Register/$',views.Register,name='Register'),
	url(r'^register/$',views.register,name='register'),
	url(r'^signin/$',views.signin,name='signin'),
	url(r'^signout/$',views.signout,name='signout'),
	url(r'^dashboard/$',views.dashboard,name='dashboard'),
]