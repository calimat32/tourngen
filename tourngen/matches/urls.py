from django.conf.urls import patterns, include, url

urlpatterns = patterns ('',

url(r'^all/$' , 'matches.views.listado'),
url(r'^guest/$','matches.views.listadovisita'),
url(r'^guestfilter','matches.views.filterguestmatches'),
url(r'^success/$', 'matches.views.success'),
url(r'^standings/$','matches.views.createstandings'),
url(r'^filter/$', 'matches.views.filtermatches'),
)