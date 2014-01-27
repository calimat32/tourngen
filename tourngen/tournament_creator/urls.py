from django.conf.urls import patterns, include, url


urlpatterns = patterns ('',
url(r'^create/$' , 'tournament_creator.views.create'),
url(r'^all/$' , 'tournament_creator.views.tournaments'),
url(r'^delete/$','tournament_creator.views.deletetournament'),
url(r'^get/(?P<tournament_id>\d+)/$', 'tournament_creator.views.tournament'),
)
