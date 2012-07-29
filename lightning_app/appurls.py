from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('lightning_app.views',
    
    url(r'^$', 'index', name='index'),
    
    url(r'^login/$', login, kwargs=dict(template_name='login.html'),
        name='login'),
    url(r'^logout/$', logout, kwargs=dict(next_page='/'),
        name='logout'),
    url(r'^login_redirect/$', 'login_redirect', name='login_redirect'),

    url(r'^register/$', 'register', name='register'),
    url(r'^photos/$', 'photos', name='photos'),
    url(r'^account/$', 'account', name='account'),
    url(r'^reg3/$', 'reg3', name='reg3'),

    url(r'^users/(.*)/$', 'users'),
    
    url(r'^(.*)/$', 'show', name='show')

)
