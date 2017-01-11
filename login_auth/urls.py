from django.conf.urls import url,include
from django.views.generic import RedirectView
from . import views

urlpatterns = [
	url(r'^$',RedirectView.as_view(url='/conference/treat17/')),
	url(r'^Register/$',views.Register,name='Register'),
	url(r'^register/$',views.register,name='register'),
	url(r'^signin$',views.signin,name='signin'),
	url(r'^signin/$',views.signin,name='signin'),
	url(r'^signout/$',views.signout,name='signout'),
	url(r'^dashboard/$',RedirectView.as_view(url='/conference/treat17/')),
	url(r'^profile/(?P<type>[0-9])/$', views.profile, name='profile'),
]