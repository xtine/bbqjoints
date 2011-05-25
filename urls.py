from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('joints.views',
    (r'^joint/(?P<joint_id>\d+)/review', 'review'),
    (r'^joint/(?P<joint_id>\d+)/', 'joint'),
    (r'^joints/(?P<state_abbr>\w+)/$', 'state'),
    (r'^joints/$', 'states'),
    (r'^search/$', 'search'),
    (r'^$', 'index'),
)

urlpatterns += patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^user/', include('registration.urls')),
    (r'^contact/', include('contact_form.urls')),
)

if settings.LOCAL_MEDIA:
    urlpatterns +=patterns('',
        (r'^static/(.+)', 'django.views.static.serve', { 'document_root' : settings.STATIC_ROOT })
    )