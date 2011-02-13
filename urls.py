from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('joints.views',
    (r'^joint/(?P<joint_id>\d+)/', 'joint'),
    (r'^joints/(?P<state_abbr>\w+)/$', 'state'),
    (r'^$', 'index'),
)

urlpatterns += patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^user/', include('registration.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': '/Users/xtine/django/bbq/media/', 'show_indexes': True}),
)