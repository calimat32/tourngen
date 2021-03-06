from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView
from django.template import RequestContext
from forms import FixtureForm
from django.http import HttpResponseRedirect 
from django.core.context_processors import csrf 
from tournament_creator.models import Fixture, Tournament, Team , Match
import itertools
from django.db import connection
from guardian.shortcuts import assign_perm, get_objects_for_user
from django.contrib.auth.decorators import permission_required

def create(request):
	if request.POST:
		form = FixtureForm(request.POST)
		if form.is_valid():
			form.save()
			
			return HttpResponseRedirect('/fixture/all')
	else:
		form = FixtureForm()
	args = {}
	args.update(csrf(request))

	args['form'] = form
	
	return render_to_response('create_fixture.html', args)

@permission_required('tournament_creator.add_match')
def fixtures(request):
	return render_to_response('fixtures.html',
				{'fixtures': Fixture.objects.all(),
                 'tournaments': get_objects_for_user(request.user,'tournament_creator.view_tournament')})

def fixture(request,fixture_id=1):
	return render_to_response('fixture.html', {'fixture':Fixture.objects.get(fixture_id=fixture_id) })

def filterfixtures(request):
    myrequest = request.GET.get('equipolocal')
    torneosfiltrados = request.GET.get('torneos')
    dict = {     'tournaments': Tournament.objects.filter(active="true"),
                 'numberofteams' : Team.objects.filter(tournament_id=torneosfiltrados).count(),
                'teams': Team.objects.filter(tournament_id=torneosfiltrados),
                'fixtures': Fixture.objects.filter(tournament_id=torneosfiltrados),
                'unito': myrequest,
                'selected_tournament':Tournament.objects.get(tournament_id=torneosfiltrados),
                'tournid':request.get_full_path()[-1:]}







    return render_to_response('filterfixture.html',
            dict)


def creatematches(request):
    myrequest = request.GET.get('equipolocal')
    torneosfiltrados = request.GET.get('torneos')
    fixturefiltrado = request.GET.get('jornada')
    dict = {     'tournaments': Tournament.objects.filter(active="true"),
                 'numberofteams' : Team.objects.filter(tournament_id=torneosfiltrados).count(),
                'teams': Team.objects.filter(tournament_id=torneosfiltrados),
                'unito': myrequest,
                'tournid':torneosfiltrados,
                'fixtures': Fixture.objects.filter(tournament_id=torneosfiltrados),

                'selected_tournament':Tournament.objects.get(tournament_id=torneosfiltrados)}


    #Crea los partidos de forma automatica, si es que el torneo es de ida y vuelta entonces crea permutaciones, si el partido
    # no es de ida y vuelta entonces crea combinaciones.

    count = 1

    if Tournament.objects.get(tournament_id=torneosfiltrados).home_and_away == 0:
         matches = list(itertools.combinations(dict['teams'],2))
         dict['partidos'] = matches
         home = list()
         visit = list()
         for i,j in matches:
          home.append(i)
          print "vs"
          visit.append(j)


         for i in range(len(home)):
          partidocreado = Match()
          fixture = Fixture()
          fixture.tournament = Tournament.objects.get(tournament_id=dict['tournid'])
          fixture.number = count +1
          fixture.Active = "true"
          count = count +1
          fixture.save()

          partidocreado.fixture = fixture
          partidocreado.home = Team.objects.get(team_id=home[i].team_id)
          partidocreado.away = Team.objects.get(team_id=visit[i].team_id)
          partidocreado.score_home = 0
          partidocreado.score_away = 0
          partidocreado.played = 0
          partidocreado.save()

         dict['local']=home[i]
         dict['visita']=visit[i]

    elif Tournament.objects.get(tournament_id=torneosfiltrados).home_and_away == 1:
         matches = list(itertools.permutations(dict['teams'],2))
         dict['partidos'] = matches
         home = list()
         visit = list()
         for i,j in matches:
          home.append(i)
          print "vs"
          visit.append(j)
          print "enter perm"

         for i in range(len(home)):
          partidocreado = Match()
          fixture = Fixture()
          fixture.tournament = Tournament.objects.get(tournament_id=dict['tournid'])
          fixture.number = count
          fixture.Active = "true"
          count = count + 1
          fixture.save()

          partidocreado.fixture = fixture
          partidocreado.home = Team.objects.get(team_id=home[i].team_id)
          partidocreado.away = Team.objects.get(team_id=visit[i].team_id)
          partidocreado.score_home = 0
          partidocreado.score_away = 0
          partidocreado.played = 0
          partidocreado.save()

         dict['local']=home[i]
         dict['visita']=visit[i]



    print list(itertools.permutations(dict['teams'],2))


    return render_to_response('matchmaker.html',
            dict)

