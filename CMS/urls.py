from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/',include('login_auth.urls')),
    url(r'^conference/',include('conference.urls')),
]
