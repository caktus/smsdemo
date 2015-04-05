from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from rapidsms.views import dashboard


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # RapidSMS core URLs
    url(r'^accounts/', include('rapidsms.urls.login_logout')),
    url(r'^$', dashboard, name='rapidsms-dashboard'),
    # RapidSMS contrib app URLs
    url(r'^messagelog/', include('rapidsms.contrib.messagelog.urls')),
    # Third party URLs
    url(r'^selectable/', include('selectable.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^httptester/', include('rapidsms.contrib.httptester.urls')),
    ]
