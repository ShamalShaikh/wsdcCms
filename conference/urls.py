from django.conf.urls import url,include
from . import views

urlpatterns = [
	# url(r'^treat17/$',views.treat),
	# url(r'^treat17/about/$',views.treatabout),
	# url(r'^treat17/links/$',views.treatlinks),
	url(r'^nhtff2020/$',views.nhtff),
	url(r'^nhtff2020/about/$',views.nhtffabout),
	url(r'^nhtff2020/links/$',views.nhtfflinks),
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
	#ITCSD2019
	url(r'^itcsd2019/$',views.itcsd),
	url(r'^itcsd2019/about/$',views.itcsdabout),
	url(r'^itcsd2019/links/$',views.itcsdlinks),
	#ITCSD2019
	url(r'^icam2019/$',views.icam),
	url(r'^icam2019/about/$',views.icamabout),
	url(r'^icam2019/links/$',views.icamlinks),
	#EWCTI2018
	url(r'^ewcti2018/$',views.ewcti),
	url(r'^ewcti2018/about/$',views.ewctiabout),
	url(r'^ewcti2018/links/$',views.ewctilinks),
	url(r'^ewcti2018/hotels/$',views.ewctihotels),
	url(r'^ewcti2018/apply$$',views.ewctiapply),
	url(r'^ewcti2018/profiles/$',views.ewctiprofiles),
    #tssc2018
	url(r'^tssc2018/$',views.tssc),
	url(r'^tssc2018/about/$',views.tsscabout),
	url(r'^tssc2018/links/$',views.tssclinks),
	url(r'^tssc2018/hotels/$',views.tsschotels),
	url(r'^tssc2018/apply/$',views.tsscapply),
	#noieas2019
	url(r'^NOIEAS-2019/$',views.noieas),
	url(r'^NOIEAS-2019/about/$',views.noieasabout),
	url(r'^NOIEAS-2019/links/$',views.noieaslinks),
	url(r'^NOIEAS-2019/hotels/$',views.noieashotels),
	url(r'^NOIEAS-2019/apply$$',views.noieasapply),

	#inceee2019
	url(r'^inceee2019/$',views.inceee),
	url(r'^inceee2019/about/$',views.inceeeabout),
	url(r'^inceee2019/links/$',views.inceeelinks),
	url(r'^inceee2019/hotels/$',views.inceeehotels),
	url(r'^inceee2019/accomodation/$', views.inceeeaccomodation),
	#url(r'^inceee2019/apply/$',views.inceeeapply),

	#sep2019 dated 04-dec-2018 Bhargava Reddy
	url(r'^sep2019/$',views.sep),
	url(r'^sep2019/about/$',views.sepabout),
	url(r'^sep2019/links/$',views.seplinks),
	url(r'^sep2019/hotels/$',views.sephotels),
	url(r'^sep2019/apply/$',views.sepapply),


	#icamer2019
	url(r'^icamer2019/$', views.icamer),
	url(r'^icamer2019/about/$', views.icamerabout),
	url(r'^icamer2019/links/$', views.icamerlinks),
	url(r'^icamer2019/hotels/$', views.icamerhotels),
	url(r'^icamer2019/dates/$', views.icamerdates),
	url(r'^icamer2019/fees/$', views.icamerfees),
	# ic2sv
	url(r'^ic2sv/$',views.ic2sv),
	url(r'^ic2sv/about/$',views.ic2svabout),
	url(r'^ic2sv/links/$',views.ic2svlinks),
	url(r'^ic2sv/hotels/$',views.ic2svhotels),
	url(r'^ic2sv/apply/$',views.ic2svapply),

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
