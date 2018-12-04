from django.conf.urls import url,include
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    #CMFD-2019
	url(r'^$',RedirectView.as_view(url='/conference/cmfdp2019/')),
	url(r'^cmfdp/$',RedirectView.as_view(url='/conference/cmfdp2019/')),
	url(r'^cmfdp2019/$',RedirectView.as_view(url='/conference/cmfdp2019/')),
	#ewcti2018
	url(r'^ewcti/$',RedirectView.as_view(url='/conference/ewcti2018/')),
	url(r'^ewcti2018/$',RedirectView.as_view(url='/conference/ewcti2018/')),
	#TSSC-2018
	url(r'^tssc/$',RedirectView.as_view(url='/conference/tssc2018/')),
	url(r'^tssc2018/$',RedirectView.as_view(url='/conference/tssc2018/')),

	#TSSC-2018
	url(r'^inceee/$',RedirectView.as_view(url='/conference/inceee2019/')),
	url(r'^inceee2019/$',RedirectView.as_view(url='/conference/inceee2019/')),
	#SEP2019
	url(r'^sep2019/$',RedirectView.as_view(url='/conference/sep2019/')),

	# url(r'^fccm/$',RedirectView.as_view(url='/conference/fccm2018/')),
	# url(r'^fccm2018/$',RedirectView.as_view(url='/conference/fccm2018/')),
	# url(r'^mmse/$',RedirectView.as_view(url='/conference/mmse2018/')),
	# url(r'^mmse2018/$',RedirectView.as_view(url='/conference/mmse2018/')),
	# url(r'^ctsem/$',RedirectView.as_view(url='/conference/ctsem2018/')),
	# url(r'^ctsem2018/$',RedirectView.as_view(url='/conference/ctsem2018/')),
	# url(r'^rames/$',RedirectView.as_view(url='/conference/rames2018/')),
	# url(r'^rames2018/$',RedirectView.as_view(url='/conference/rames2018/')),
	# url(r'^nhtff2018/$',RedirectView.as_view(url='/conference/nhtff2018/')),
	# url(r'^treat2017/$',RedirectView.as_view(url='/conference/treat17/')),
	#url(r'^Register/(?P<alias>[A-Za-z0-9.-]+)/$',views.Register,name='Register'),
	url(r'^register/(?P<alias>[A-Za-z0-9.-]+)/$',views.register,name='register'),
	url(r'^registerspons/(?P<alias>[A-Za-z0-9.-]+)/$',views.registerSpons,name='registerSpons'),

	url(r'^signin/(?P<alias>[A-Za-z0-9.-]+)/$',views.signin,name='signin'),
	#url(r'^signin/(?P<alias>[A-Za-z0-9.-]+)/$',views.signin,name='signin'),
	url(r'^signout/(?P<alias>[A-Za-z0-9.-]+)/$',views.signout,name='signout'),
	# url(r'^dashboard/$',RedirectView.as_view(url='/conference/mmse2018/')),
	url(r'^dashboard/(?P<alias>[A-Za-z0-9.-]+)/$',views.dashboard,name='dashboard'),
	#url(r'^profile/(?P<type>[0-9])/$', views.profile, name='profile'),
	url(r'^downloaddd/(?P<payment_id>[A-Za-z0-9.-]+)/$',views.dddownload,name='downloaddd'),
	url(r'^downloadid/(?P<payment_id>[A-Za-z0-9.-]+)/$',views.iddownload,name='downloadid'),
	url(r'^downloadrejdd/(?P<rej_payment_id>[A-Za-z0-9.-]+)/$',views.rejectedpaymentdownload,name='rejectedpaymentdownload'),
]
