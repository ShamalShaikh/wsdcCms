from django.conf.urls import url,include
from django.conf import settings
from django.conf.urls.static import static
from reviews import views

urlpatterns = [
	url(r'^$', views.reviewHome),
	url(r'^login/$', views.loginReviewer),
	url(r'^logout/$', views.logoutReviewer),
	url(r'^404/$', views.err404),
	url(r'^downloadpaper/(?P<paper_id>[A-Za-z0-9.-]+)/$',views.paperdownload),
	url(r'^reviewPaper/(?P<paper_id>[A-Za-z0-9.-]+)/$',views.reviewPaper),
	url(r'^assignMarks/(?P<ansid>[A-Za-z0-9.-]+)/$',views.assignMarks),
	url(r'^submitRemark/(?P<paper_id>[A-Za-z0-9.-]+)/$',views.submitRemark),
	url(r'^submitReview/(?P<paper_id>[A-Za-z0-9.-]+)/$',views.submitReview),
]