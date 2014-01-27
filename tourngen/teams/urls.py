from django.conf.urls import patterns, include, url
from teams.views import RegisterTeam


urlpatterns = patterns ('',
url(r'^create/$' , 'teams.views.create'),
url(r'^register/$',RegisterTeam.as_view(), name="register_team"),
url(r'^all/$' , 'teams.views.teams'),
url(r'^filter/$', 'teams.views.filterteams'),
url(r'^delete/$', 'teams.views.deleteteam'),
url(r'^get/(?P<team_id>\d+)/$', 'teams.views.team'),
)
