
from django.shortcuts import render, render_to_response
from tournament_creator.models import Team, Tournament, Fixture, Match
from django.db.models import Sum
import operator

# Create your views here.
def listado(request):
    idpartido = request.GET.get('partido_id')
    puntajelocal = request.GET.get('score_local')
    puntajevisita = request.GET.get('score_visita')


   # partido = Match.objects.get(match_id=idpartido)
   # partido.score_home = puntajelocal
   # partido.score_away = puntajevisita
   # partido.save()

    print idpartido
    dict = {'partidos': Match.objects.all(),
            'tournaments': Tournament.objects.filter(active="true")}

    return render_to_response('matchviewer.html',dict)


def success(request):
    idpartido = request.GET.get('partido_id')
    puntajelocal = request.GET.get('score_local')
    puntajevisita = request.GET.get('score_visita')


    partido = Match.objects.get(match_id=idpartido)
    partido.score_home = puntajelocal
    partido.score_away = puntajevisita
    partido.save()

    print idpartido
    dict = {'partidos': Match.objects.all(),
            'tournaments': Tournament.objects.filter(active="true")}

    return render_to_response('matchsuccess.html',dict)

def filtermatches(request):
    myrequest = "salsa"
    torneosfiltrados = request.GET.get('torneos')
    dict = {     'tournaments': Tournament.objects.filter(active="true"),
                 'numberofteams' : Team.objects.filter(tournament_id=request.get_full_path()[-1:]).count(),
                'teams': Team.objects.filter(tournament_id=torneosfiltrados),
                'fixtures': Fixture.objects.filter(tournament_id=torneosfiltrados),
                'unito': myrequest,
                'selected_tournament':Tournament.objects.get(tournament_id=torneosfiltrados),

                'tournid':request.get_full_path()[-1:]}

    equipos = Team.objects.filter(tournament_id=torneosfiltrados)
    dict['partidos'] = Match.objects.filter(fixture_id=dict['fixtures'])






    return render_to_response('filtermatch.html',
            dict)

def createstandings(request):
    myrequest = "salsa"
    torneosfiltrados = request.GET.get('torneos')
    dict = {     'tournaments': Tournament.objects.filter(active="true"),
                 'teams': Team.objects.filter(tournament_id=torneosfiltrados),
                'fixtures': Fixture.objects.filter(tournament_id=torneosfiltrados),
                'unito': myrequest,
                'selected_tournament':Tournament.objects.get(tournament_id=torneosfiltrados)}

    equipos = Team.objects.filter(tournament_id=torneosfiltrados)
    dict['partidos'] = Match.objects.filter(fixture_id=dict['fixtures'])


    totalpoints = 0
    totalhomescoreslist = list()
    totalawayscoreslist = list()
    totalgoalagainst = list()
    totalgoalfavor = list()
    homelist = list()
    againsthomescoreslist = list()
    againstawayscoreslist = list()

    for item in range(len(equipos)):
        partidostanding = Match.objects.filter(fixture_id=dict['fixtures'],home=equipos[item].team_id)
        partidostandingaway = Match.objects.filter(fixture_id=dict['fixtures'], away = equipos[item].team_id)
        totalhomescores = partidostanding.aggregate(Sum('score_home'))
        againsthomescores = partidostanding.aggregate(Sum('score_away'))
        totalawayscores = partidostandingaway.aggregate(Sum('score_away'))
        againstawayscores = partidostandingaway.aggregate(Sum('score_home'))
        totalhomescoreslist.append(totalhomescores['score_home__sum'])
        againstawayscoreslist.append(againstawayscores['score_home__sum'])
        againsthomescoreslist.append(againsthomescores['score_away__sum'])
        totalawayscoreslist.append(totalawayscores['score_away__sum'])
        if totalhomescoreslist[item]== None:
            totalhomescoreslist[item]=0
        if totalawayscoreslist[item] == None:
            totalawayscoreslist[item] = 0
        if againsthomescoreslist[item] == None:
            againsthomescoreslist[item] = 0
        if againstawayscoreslist[item] == None:
            againstawayscoreslist[item] = 0



    totalgoalfavor = map(operator.add, totalhomescoreslist,totalawayscoreslist)
    totalgoalagainst = map(operator.add,againsthomescoreslist,againstawayscoreslist)

    dict['puntajesvista'] = totalawayscoreslist
    dict['puntajeslocales'] = totalhomescoreslist
    dict['golesafavor'] = totalgoalfavor
    dict['golesencontra'] = totalgoalagainst
    print totalhomescoreslist




    return render_to_response('standings.html',
            dict)