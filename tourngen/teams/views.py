from django.shortcuts import render
from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView, ListView
from django.template import RequestContext
from forms import TeamForm
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from tournament_creator.models import Team, Tournament, Fixture, Match
from django.db.models import Count
from guardian.shortcuts import assign_perm, get_objects_for_user
from django.views.generic import CreateView
from django.contrib.auth.decorators import permission_required
import pprint

# Create your views here.


#class ReportarEquipos(ListView):
#       model = Tournament
#      template_name = 'teams.html'

class RegisterTeam(CreateView):
    template_name='create_team.html'

    model = Team

    success_url = ('/team/all')


@permission_required('tournament_creator.add_team')
def create(request):
    if request.POST:
        form = TeamForm(request.POST)


        if form.is_valid():
            team = form.save()
            user = request.user
            assign_perm('view_team', user, team)

            return HttpResponseRedirect('/team/all')
    else:
        form = TeamForm()
    args = {}
    args.update(csrf(request))

    #form.fields['tournament'] = Tournament.objects.all()

    args['form'] = form
    args['form'].fields['tournament']= get_objects_for_user(request.user , 'tournament_creator.view_tournament')
    args['tournament'] = Tournament.objects.all()


    return render_to_response('create_team.html', args)

@permission_required('tournament_creator.delete_team')
def teams(request):
    return render_to_response('teams.html',
                              {'teams': Team.objects.all(),
                               'tournaments': get_objects_for_user(request.user,'tournament_creator.view_tournament'),
                               'currentURL': Team.objects.count()
                              })

#Vista para eliminar equipos
@permission_required('tournament_creator.delete_team')
def deleteteam(request):
    dict = {}
    idteam = request.GET.get('team')
    team = Team.objects.get(team_id = idteam)

    team.delete()
    return render_to_response('deleteteam.html',dict)


def filterteams(request):
    torneosfiltrados = request.GET.get('torneos')
    dict = {'tournaments': Tournament.objects.filter(active="true"),
            'numberofteams': Team.objects.filter(tournament_id=torneosfiltrados).count(),
            'teams': Team.objects.filter(tournament_id=torneosfiltrados),
            'tournid': torneosfiltrados}

    #Crea los fixtures necesarios para poder crear los partidos. Si el numero de equipos es impar entonces
    #crea el mismo numero de fixtures para el numero de equipos. Si el numero de equipos es par entonces
    #crea el un fixture menos del numero de equipos solicitado.
    count = 1

    if dict['numberofteams'] > 0 and dict['numberofteams'] % 2 != 0:
        for item in range(dict['numberofteams']):
            fixture = Fixture()
            fixture.tournament = Tournament.objects.get(tournament_id=dict['tournid'])
            fixture.number = count
            fixture.Active = "true"
            count = count + 1
            fixture.save()

    elif dict['numberofteams'] > 0 and dict['numberofteams'] % 2 == 0:
        for item in range(dict['numberofteams'] - 1):
            fixture = Fixture()
            fixture.tournament = Tournament.objects.get(tournament_id=dict['tournid'])
            fixture.number = count
            fixture.Active = "true"
            count = count + 1
            fixture.save()

    return render_to_response('filter.html',
                              dict)

@permission_required('tournament_creator.delete_team')
def team(request, team_id=1):
    return render_to_response('team.html', {'team': Team.objects.get(team_id=team_id)})



