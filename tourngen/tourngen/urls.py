from django.conf.urls import patterns, include, url
from django.contrib import admin
from tournament_creator.views import Usuario
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

admin.autodiscover()



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tourngen.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url  (r'^$', 'django.contrib.auth.views.login', {'template_name':'index.html'} ,    name='login'),	
    
    url  (r'^logout/$', 'django.contrib.auth.views.logout_then_login',     name='logout'),	

(r'^matches/', TemplateView.as_view(template_name="matches.html")),

url(r'^tournament/', include('tournament_creator.urls')),
url(r'^team/', include('teams.urls')),
url(r'^fixture/', include('fixtures.urls')),
url(r'^match/',include('matches.urls')),

 #   url  (r'^accounts/profile', 
  #     TemplateView.as_view(template_name='profile.html'),
   #     name='profile'),	
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    #url(r'^accounts/profile', RedirectView.as_view(url='/'}),	
   url(r'^users/(?P<usuario>[-\w]+)/$', Usuario.as_view())

)

LOGIN_REDIRECT_URL = reverse_lazy('index')
