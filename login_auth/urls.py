from django.conf.urls import url,include
from django.views.generic import RedirectView
from . import views

urlpatterns = [
	url(r'^$',RedirectView.as_view(url='/conference/nhtff2018/')),
	url(r'^nhtff2018/$',RedirectView.as_view(url='/conference/nhtff2018/')),
	url(r'^treat2017/$',RedirectView.as_view(url='/conference/treat17/')),
	url(r'^Register/$',views.Register,name='Register'),
	url(r'^register/$',views.register,name='register'),
	url(r'^signin$',views.signin,name='signin'),
	url(r'^signin/$',views.signin,name='signin'),
	url(r'^signout/$',views.signout,name='signout'),
	url(r'^dashboard/$',RedirectView.as_view(url='/conference/treat17/')),
	url(r'^profile/(?P<type>[0-9])/$', views.profile, name='profile'),
	url(r'^downloaddd/(?P<payment_id>[A-Za-z0-9.-]+)/$',views.dddownload,name='downloaddd'),
	url(r'^downloadid/(?P<payment_id>[A-Za-z0-9.-]+)/$',views.iddownload,name='downloadid'),
	url(r'^downloadrejdd/(?P<rej_payment_id>[A-Za-z0-9.-]+)/$',views.rejectedpaymentdownload,name='rejectedpaymentdownload'),
]