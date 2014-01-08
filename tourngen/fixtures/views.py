from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView
from django.template import RequestContext
from forms import FixtureForm
from django.http import HttpResponseRedirect 
from django.core.context_processors import csrf 
from tournament_creator.models import Fixture, Tournament, Team , Match
import itertools
from django.db import connection


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

def fixtures(request):
	return render_to_response('fixtures.html',
				{'fixtures': Fixture.objects.all(),
                 'tournaments': Tournament.objects.filter(active="true")})

def fixture(request,fixture_id=1):
	return render_to_response('fixture.html', {'fixture':Fixture.objects.get(fixture_id=fixture_id) })

def filterfixtures(request):
    myrequest = request.GET.get('equipolocal')
    torneosfiltrados = request.GET.get('torneos')
    dict = {     'tournaments': Tournament.objects.filter(active="true"),
                 'numberofteams' : Team.objects.filter(tournament_id=request.get_full_path()[-1:]).count(),
                'teams': Team.objects.filter(tournament_id=request.get_full_path()[-1:]),
                'fixtures': Fixture.objects.filter(tournament_id=request.get_full_path()[-1:]),
                'unito': myrequest,
                'selected_tournament':Tournament.objects.get(tournament_id=torneosfiltrados),
                'tournid':request.get_full_path()[-1:]}



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

        dict['local']=home[i]
        dict['visita']=visit[i]

    dict['visitante'] =visit
    print "partidos"
    print home[3]
    print "hello"
    print visit
    print torneosfiltrados
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
                'tournid':request.get_full_path()[-1:],
                'fixtures': Fixture.objects.filter(tournament_id=torneosfiltrados),
                'fixture_filter':Fixture.objects.get(fixture_id=fixturefiltrado),
                'selected_tournament':Tournament.objects.get(tournament_id=1)}

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
        partidocreado.fixture = Fixture.objects.get(fixture_id=fixturefiltrado)
        partidocreado.home = Team.objects.get(team_id=home[i].team_id)
        partidocreado.away = Team.objects.get(team_id=visit[i].team_id)
        partidocreado.score_home = 0
        partidocreado.score_away = 0 
        partidocreado.save()
    return render_to_response('matchmaker.html',
            dict)

