from django.conf.urls import patterns, include, url

urlpatterns = patterns ('',
url(r'^create/$' , 'fixtures.views.create'),
url(r'^all/$' , 'fixtures.views.fixtures'),
url(r'^filter/$', 'fixtures.views.filterfixtures'),
url(r'^matchmaker/$','fixtures.views.creatematches'),
url(r'^get/(?P<fixture_id>\d+)/$', 'fixtures.views.fixture'),
)
