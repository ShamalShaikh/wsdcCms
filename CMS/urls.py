from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from conference.views import gian, home, bctfcs,bctfcsabout,bctfcslinks,bctfcsregister

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('',include('login_auth.urls')),
    url(r'^conference/',include('conference.urls')),
    url(r'^review/', include('reviews.urls')),
    url(r'^manager/', include('manager.urls')),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^gian/$', gian ),
    url(r'^bctfcs/$', bctfcs),
    url(r'^bctfcs/about/$', bctfcsabout),
    url(r'^bctfcs/links/$', bctfcslinks),
    url(r'^bctfcs/register/$', bctfcsregister),
    url(r'^$',home)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)