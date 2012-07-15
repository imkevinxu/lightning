from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('lightning_app.views',
    
    url(r'^$', 'index', name='index'),
    url(r'^search/$', 'search', name='search'),
    
    url(r'^login/$', login, kwargs=dict(template_name='login.html'),
        name='login'),
    url(r'^logout/$', logout, kwargs=dict(next_page='/'),
        name='logout'),

    url(r'^reg1/$', 'reg1', name='reg1'),
    url(r'^reg2/$', 'reg2', name='reg2'),
    url(r'^reg3/$', 'reg3', name='reg3'),
    url(r'^photog/$', 'photog', name='photog'),

)
