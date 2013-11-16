from django.conf.urls import patterns, include, url
from django.contrib import admin
from tournament_creator.views import Usuario

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tourngen.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.simple.urls')),
   url(r'^users/(?P<usuario>[-\w]+)/$', Usuario.as_view())
	
)
