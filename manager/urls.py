from django.conf.urls import url,include
from manager import views

urlpatterns = [
	url(r'^$', views.home),
	url(r'^assignreviewer/', views.assign_reviewer),
]