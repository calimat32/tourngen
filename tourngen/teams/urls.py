from django.conf.urls import patterns, include, url

urlpatterns = patterns ('',
url(r'^create/$' , 'teams.views.create'),
url(r'^all/$' , 'teams.views.teams'),  
url(r'^get/(?P<team_id>\d+)/$', 'teams.views.team'),
)
