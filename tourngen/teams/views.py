from django.shortcuts import render
from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView, ListView
from django.template import RequestContext
from forms import TeamForm
from django.http import HttpResponseRedirect 
from django.core.context_processors import csrf 
from tournament_creator.models import Team, Tournament, Fixture, Match
from django.db.models import Count
from guardian.shortcuts import get_objects_for_user


# Create your views here.


#class ReportarEquipos(ListView):
 #       model = Tournament
  #      template_name = 'teams.html'


def create(request):
	if request.POST:
		form = TeamForm(request.POST)
		if form.is_valid():
			form.save()

			return HttpResponseRedirect('/team/all')
	else:
		form = TeamForm()
	args = {}
	args.update(csrf(request))

	args['form'] = form

	
	return render_to_response('create_team.html', args)

def teams(request):
               return render_to_response('teams.html',
				{'teams': Team.objects.all(),
                 'tournaments': get_objects_for_user(request.user,'tournament_creator.change_tournament'),
                 'currentURL':Team.objects.count()
                 })

def filterteams(request):
    torneosfiltrados = request.GET.get('torneos')
    dict = {     'tournaments': Tournament.objects.filter(active="true"),
                 'numberofteams' : Team.objects.filter(tournament_id=torneosfiltrados).count(),
                'teams': Team.objects.filter(tournament_id=torneosfiltrados),
                'tournid':torneosfiltrados}

    #Crea los fixtures necesarios para poder crear los partidos. Si el numero de equipos es impar entonces
    #crea el mismo numero de fixtures para el numero de equipos. Si el numero de equipos es par entonces
    #crea el un fixture menos del numero de equipos solicitado.
    count = 1


    if dict['numberofteams']>0 and dict['numberofteams']%2!=0:
        for item in range(dict['numberofteams']):
         fixture = Fixture()
         fixture.tournament = Tournament.objects.get(tournament_id=dict['tournid'])
         fixture.number = count
         fixture.Active = "true"
         count = count +1
         fixture.save()

    elif dict['numberofteams']>0 and dict['numberofteams']%2==0:
         for item in range(dict['numberofteams']-1):
          fixture = Fixture()
          fixture.tournament = Tournament.objects.get(tournament_id=dict['tournid'])
          fixture.number = count
          fixture.Active = "true"
          count = count +1
          fixture.save()



    return render_to_response('filter.html',
            dict)



def team(request,team_id=1):
	return render_to_response('team.html', {'team':Team.objects.get(team_id=team_id) })



