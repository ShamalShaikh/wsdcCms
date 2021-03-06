from django.conf.urls import url,include
from manager import views

urlpatterns = [
	url(r'^assignreviewer/(?P<paper_id>[A-Za-z0-9.-]+)/$', views.assign_reviewer),
	url(r'^reviewcomplete/(?P<paper_id>[A-Za-z0-9.-]+)/(?P<u_id>[A-Za-z0-9.-]+)/$', views.reviewCompleted),
	url(r'^$',views.home),
	url(r'^signin/$',views.signin,name='signin'),
	url(r'^signin_auth/$',views.signin_auth,name='signin_auth'),
	url(r'^signout/$',views.signout,name='signout'),
	url(r'^assignreviewer/$', views.assign_reviewer),
	url(r'^reviewerassigned/(?P<paper_id>[A-Za-z0-9.-]+)/(?P<u_id>[A-Za-z0-9.-]+)/$', views.reviewerAssigned),
	url(r'^allresponses/(?P<paper_id>[A-Za-z0-9.-]+)/$', views.averageResponses),
	url(r'^conference_landing/(?P<cid>[0-9]+)/(?P<type>[0-9])/$',views.conference_landing,name='conference_landing'),
	url(r'^approve_payment/(?P<payid>[0-9]+)/$',views.approve_payment,name='approve_payment'),
	url(r'^disapproval/$',views.disapproval,name='disapproval'),
	url(r'^questionnaire/(?P<cid>[0-9]+)/$',views.questionnaire,name='questionnaire'),
	url(r'^approvepaper/(?P<type>[0-9]+)/(?P<paper_id>[A-Za-z0-9.-]+)/$', views.isApprovedPaper),
	url(r'^disapprovepaper/(?P<paper_id>[A-Za-z0-9.-]+)/$', views.isDisapprovedPaper),
	url(r'^exportdata/(?P<cid>[0-9]+)/$', views.export_xls),
	url(r'^conference_landing/(?P<cid>[0-9]+)/(?P<type>[0-9])/sendmail/$', views.sendmail),
	url(r'^paper_remark/(?P<paper_id>[A-Za-z0-9.-]+)/$', views.paper_remark),
	##reviewUrls
	url(r'^assignToReview/(?P<paper_id>[A-Za-z0-9.-]+)/$',views.assignToReview),
	url(r'^reviewDetails/(?P<revid>[0-9]+)/$',views.reviewDetails),
	url(r'^reassign/(?P<revid>[0-9]+)/$',views.reassign),
	url(r'^contestantList/$',views.contestantList),
	url(r'^accomo/$', views.approveaccomo),
	url(r'^exportaccomo/$', views.accomodationData),
]
