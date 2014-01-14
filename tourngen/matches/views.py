
from django.shortcuts import render, render_to_response
from tournament_creator.models import Team, Tournament, Fixture, Match
from django.db.models import Sum, Count
import operator
import itertools

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


    victories= list()
    partidosjugadoshomelist = list()
    partidosjugadosawaylist = list()
    partidosgandoslist = list()
    totalhomescoreslist = list()
    totalawayscoreslist = list()
    totalgoalagainst = list()
    totalgoalfavor = list()
    homelist = list()
    partidosgandoslist = list()
    againsthomescoreslist = list()
    againstawayscoreslist = list()
    dummy = 0
    partidosganados =0
    partidosjugadoshome = 0
    partidosjugadosaway=0
    partidosjugadoslist = list()

    for item in range(len(equipos)):
        #Saca los goles a favor y los goles en contra
        partidostanding = Match.objects.filter(fixture_id=dict['fixtures'],home=equipos[item].team_id,played="true")
        partidostandingaway = Match.objects.filter(fixture_id=dict['fixtures'], away = equipos[item].team_id,played="true")
        totalhomescores = partidostanding.aggregate(Sum('score_home'))
        againsthomescores = partidostanding.aggregate(Sum('score_away'))
        totalawayscores = partidostandingaway.aggregate(Sum('score_away'))
        againstawayscores = partidostandingaway.aggregate(Sum('score_home'))
        totalhomescoreslist.append(totalhomescores['score_home__sum'])
        againstawayscoreslist.append(againstawayscores['score_home__sum'])
        againsthomescoreslist.append(againsthomescores['score_away__sum'])
        totalawayscoreslist.append(totalawayscores['score_away__sum'])

        for otheritem in range(len(partidostanding)):
            if partidostanding[otheritem].score_home > partidostanding[otheritem].score_away:
                print "won"
                partidosganados = partidosganados + 1

                print partidosganados
            elif partidostanding[otheritem].score_home == partidostanding[otheritem].score_away:
                print "tie"
            elif partidostanding[otheritem].score_home < partidostanding[otheritem].score_away:
                print "lost"



        for otheritem in range(len(partidostandingaway)):
            if partidostandingaway[otheritem].score_home < partidostandingaway[otheritem].score_away:
                print "won visit"
            elif partidostandingaway[otheritem].score_home == partidostandingaway[otheritem].score_away:
                print "tie visit"
            elif partidostandingaway[otheritem].score_home > partidostandingaway[otheritem].score_away:
                print "lost visit"

        partidosjugadosaway = partidosjugadosaway + 1

        partidosjugadoshomelist.append(partidostanding.count())
        partidosjugadosawaylist.append(partidostandingaway.count())

        if totalhomescoreslist[item]== None:
            totalhomescoreslist[item]=0
        if totalawayscoreslist[item] == None:
            totalawayscoreslist[item] = 0
        if againsthomescoreslist[item] == None:
            againsthomescoreslist[item] = 0
        if againstawayscoreslist[item] == None:
            againstawayscoreslist[item] = 0



    partido = Match(fixture_id=dict['fixtures'],home=equipos[0])




    nuevalista = list(itertools.izip(equipos,totalgoalfavor))
    partidosjugadoslist = map(operator.add,partidosjugadoshomelist,partidosjugadosawaylist)
    totalgoalfavor = map(operator.add, totalhomescoreslist,totalawayscoreslist)
    totalgoalagainst = map(operator.add,againsthomescoreslist,againstawayscoreslist)
    totalgoaldif = map(operator.sub, totalgoalfavor,totalgoalagainst)

    dict['puntajesvista'] = totalawayscoreslist
    dict['puntajeslocales'] = totalhomescoreslist
    dict['golesafavor'] = totalgoalfavor
    dict['golesencontra'] = totalgoalagainst
    dict['golesdiferencia'] = totalgoaldif
    dict['partidosjugados'] = partidosjugadoslist
    dict['victorias'] = victories
    print "papaya"

    print partidosjugadoslist



    return render_to_response('standings.html',
            dict)