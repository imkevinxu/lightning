from django.conf.urls.defaults import * 
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('', 
    
    #Admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    #App url include
    url(r'^', include('lightning_app.appurls')),
    #url(r'^lightning/$', include('lightning.appurls')),
    
    #Static Links
    #url(r'^', TemplateView.as_view(template_name='home.html'), name='home'),
    
)

#urlpatterns += patterns('lightning_site.lightning.views',
#   url(r'^lightning/$', 'lightning_view', name='lightning'),
#)

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )