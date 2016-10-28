from django.conf.urls import url,include
from manager import views

urlpatterns = [
	url(r'^$',views.home),
	url(r'^signin/$',views.signin,name='signin'),
	url(r'^signin_auth/$',views.signin_auth,name='signin_auth'),

]