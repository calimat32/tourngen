from django.conf.urls import patterns, include, url

urlpatterns = patterns ('',

url(r'^all/$' , 'matches.views.listado'),
url(r'^allact/$','matches.views.listadofixture'),
url(r'^guest/$','matches.views.listadovisita'),
url(r'^guestfilter','matches.views.filterguestmatches'),
url(r'^mine/$','matches.views.listadorep'),
url(r'myfilter/$','matches.views.filtermymatches'),
url(r'^success/$', 'matches.views.success'),
url(r'^standings/$','matches.views.createstandings'),
url(r'^filter/$', 'matches.views.filtermatches'),
url(r'^filteract/$','matches.views.filtermatchesact'),
url(r'^successact/$','matches.views.successact'),

)