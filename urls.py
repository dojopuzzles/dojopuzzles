from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'problemas.views.problema_aleatorio', name='problema-aleatorio'),
    url(r'^problema/$', 'problemas.views.problema_aleatorio', name='problema-aleatorio'),
    url(r'^problema/(?P<problema_id>\d+)/$', 'problemas.views.exibe_problema', name='exibe-problema'),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    url(r'^media/(.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
)
