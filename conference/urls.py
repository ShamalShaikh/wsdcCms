from django.conf.urls import url,include
from . import views

urlpatterns = [
	url(r'^treat17/$',views.treat),
	url(r'^treat17/about/$',views.treatabout),
	url(r'^treat17/links/$',views.treatlinks),
	url(r'^(?P<alias>[A-Za-z0-9.-]+)/$',views.index),
	url(r'^make_payment/(?P<alias>[A-Za-z0-9.-]+)/$',views.make_payment,name='make_payment'),
	url(r'^payment/(?P<alias>[A-Za-z0-9.-]+)/$',views.payment,name='payment'),
	url(r'^upload_paper/(?P<alias>[A-Za-z0-9.-]+)/$',views.upload_paper,name='upload_paper'),
	url(r'^upload_final_paper/(?P<alias>[A-Za-z0-9.-]+)/$',views.final_paper,name='upload_final_paper'),
	url(r'^reupload_paper/(?P<alias>[A-Za-z0-9.-]+)/$',views.reupload_paper,name='reupload_paper'),
	url(r'^(?P<alias>[A-Za-z0-9.-]+)/dashboard/$',views.dashboard,name='dashboard'),
]