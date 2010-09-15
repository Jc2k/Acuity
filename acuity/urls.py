from django.conf.urls.defaults import *
from views import dirlist

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),
    (r'^browse$', dirlist),
)
