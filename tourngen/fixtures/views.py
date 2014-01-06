from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView
from django.template import RequestContext
from forms import FixtureForm
from django.http import HttpResponseRedirect 
from django.core.context_processors import csrf 
from tournament_creator.models import Fixture, Tournament, Team
import itertools

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


    print "hello"
    print torneosfiltrados
    return render_to_response('filterfixture.html',
            dict)


def creatematches(request):
    myrequest = request.GET.get('equipolocal')
    torneosfiltrados = request.GET.get('torneos')
    dict = {     'tournaments': Tournament.objects.filter(active="true"),
                 'numberofteams' : Team.objects.filter(tournament_id=torneosfiltrados).count(),
                'teams': Team.objects.filter(tournament_id=torneosfiltrados),
                'unito': myrequest,
                'tournid':request.get_full_path()[-1:],
                'selected_tournament':Tournament.objects.get(tournament_id=1)}

    return render_to_response('matchmaker.html',
            dict)

