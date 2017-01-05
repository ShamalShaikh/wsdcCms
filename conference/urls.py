from django.conf.urls import url,include
from . import views

urlpatterns = [
	url(r'^treat17/$',views.treat),
	url(r'^treat17/about/$',views.treatabout),
	url(r'^treat17/links/$',views.treatlinks),
	url(r'^(?P<alias>[A-Za-z0-9.-]+)/$',views.index),
	url(r'^make_payment/$',views.make_payment,name='make_payment'),
	url(r'^payment/$',views.payment,name='payment'),
	url(r'^upload_paper/(?P<alias>[A-Za-z0-9.-]+)/$',views.upload_paper,name='upload_paper'),
	url(r'^(?P<alias>[A-Za-z0-9.-]+)/dashboard/$',views.dashboard,name='dashboard'),
]