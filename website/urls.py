from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'', include('website.apps.blog.urls')),
)

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$',
        'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT, 
            'show_indexes': True,
        },
    ),
)
