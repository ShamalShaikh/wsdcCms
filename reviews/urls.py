from django.conf.urls import url,include
from django.conf import settings
from django.conf.urls.static import static
from reviews import views

urlpatterns = [
	url(r'^$', views.reviewHome),
	url(r'^reviewpaper/(?P<paper_id>[A-Za-z0-9.-]+)/$', views.reviewPaper),
]