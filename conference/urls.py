from django.conf.urls import url,include
from . import views

urlpatterns = [
	url(r'^$',views.index),
	url(r'^make_payment/$',views.make_payment,name='make_payment'),
	url(r'^payment/$',views.payment,name='payment'),
]