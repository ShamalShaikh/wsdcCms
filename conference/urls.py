from django.conf.urls import url,include
from . import views

urlpatterns = [
	# url(r'^treat17/$',views.treat),
	# url(r'^treat17/about/$',views.treatabout),
	# url(r'^treat17/links/$',views.treatlinks),
	# url(r'^nhtff2018/$',views.nhtff),
	# url(r'^nhtff2018/about/$',views.nhtffabout),
	# url(r'^nhtff2018/links/$',views.nhtfflinks),
	# url(r'^mmse2018/$',views.mmse),
	# url(r'^mmse2018/about/$',views.mmseabout),
	# url(r'^mmse2018/links/$',views.mmselinks),
	# url(r'^ctsem2018/$',views.ctsem),
	# url(r'^ctsem2018/about/$',views.ctsemabout),
	# url(r'^ctsem2018/links/$',views.ctsemlinks),
	# url(r'^rames2018/$',views.rames),
	# url(r'^rames2018/about/$',views.ramesabout),
	# url(r'^rames2018/links/$',views.rameslinks),
	# url(r'^fccm2018/$',views.fccm),
	# url(r'^fccm2018/about/$',views.fccmabout),
	# url(r'^fccm2018/links/$',views.fccmlinks),

	url(r'^cmfdp2019/$',views.cmfdp),
	url(r'^cmfdp2019/about/$',views.cmfdpabout),
	url(r'^cmfdp2019/links/$',views.cmfdplinks),

	# url(r'^metallography_contest/$',views.metallography_contest),
	# url(r'^registerForContest/$',views.registerForContest),
	# url(r'^(?P<alias>[A-Za-z0-9.-]+)/$',views.index),
	
	url(r'^make_payment/(?P<alias>[A-Za-z0-9.-]+)/$',views.make_payment,name='make_payment'),
	url(r'^payment/(?P<alias>[A-Za-z0-9.-]+)/$',views.payment,name='payment'),
	url(r'^upload_paper/(?P<alias>[A-Za-z0-9.-]+)/$',views.upload_paper,name='upload_paper'),
	url(r'^upload_final_paper/(?P<alias>[A-Za-z0-9.-]+)/$',views.final_paper,name='upload_final_paper'),
	url(r'^reupload_paper/(?P<alias>[A-Za-z0-9.-]+)/$',views.reupload_paper,name='reupload_paper'),
	url(r'^(?P<alias>[A-Za-z0-9.-]+)/dashboard/$',views.dashboard,name='dashboard'),
	url(r'^downloadpaper/(?P<paper_id>[A-Za-z0-9.-]+)/$',views.paperdownload,name='paperdownload'),
	url(r'^downloadremark/(?P<paper_id>[A-Za-z0-9.-]+)/$',views.remarkdownload,name='remarkdownload'),
	url(r'^downloadfinalpaper/(?P<final_paper_id>[A-Za-z0-9.-]+)/$',views.finalpaperdownload,name='finalpaperdownload'),
	url(r'^downloadfinalcf/(?P<final_paper_id>[A-Za-z0-9.-]+)/$',views.finalcfdownload,name='finalcfdownload'),
]