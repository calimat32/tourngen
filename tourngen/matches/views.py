
from django.shortcuts import render, render_to_response
from tournament_creator.models import Team, Tournament, Fixture, Match
from django.db.models import Sum, Count, F
import operator
import itertools

# Create your views here.

#Muestra el listado de todos los partidos creados
def listado(request):

    #Obtiene los valores obtenidos por el request a traves del metodo get
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

#Muestra el template cuando un partido fue guardado los goles exitosamente.
def success(request):
    idpartido = request.GET.get('partido_id')
    puntajelocal = request.GET.get('score_local')
    puntajevisita = request.GET.get('score_visita')

    #Obtiene el partido de la id al cual el usuario cambia y despues actualiza sus puntajes,
    #despues lo guarda en la base de datos.
    partido = Match.objects.get(match_id=idpartido)
    partido.score_home = puntajelocal
    partido.score_away = puntajevisita
    partido.save()


    dict = {'partidos': Match.objects.all(),
            'tournaments': Tournament.objects.filter(active="true")}

    return render_to_response('matchsuccess.html',dict)

#Filtra los partidos dependendo del torneo al cual se le es asignado
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

#Crea la tabla de posiciones
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

   #Declaacion de variables que seran usadas despues
    victories= list()
    partidosjugadoshomelist = list()
    partidosjugadosawaylist = list()
    partidosganadoslist = list()
    totalhomescoreslist = list()
    totalawayscoreslist = list()
    totalgoalagainst = list()
    totalgoalfavor = list()
    homelist = list()
    partidosgandoslist = list()
    againsthomescoreslist = list()
    againstawayscoreslist = list()
    partidosganadoshomelist = list()
    partidosganadosawaylist = list()
    dummy = 0
    partidosganadoshome =0
    partidosjugadoshome = 0
    partidosjugadosaway=0
    partidosjugadoslist = list()

    for item in range(len(equipos)):
        #Saca los goles a favor y los goles en contra, partidostanding son todos los partidos que tengan a cada equipo
        #como equipo local y partidostandingaway son todos los partidos que tengan a cada equipo como equipo visita.
        partidostanding = Match.objects.filter(fixture_id=dict['fixtures'],home=equipos[item].team_id,played="true")
        partidostandingaway = Match.objects.filter(fixture_id=dict['fixtures'], away = equipos[item].team_id,played="true")

        #Hace las sumas de los goles para local y para visita dependiendo de si el equipo es local o es visita
        totalhomescores = partidostanding.aggregate(Sum('score_home'))
        againsthomescores = partidostanding.aggregate(Sum('score_away'))
        totalawayscores = partidostandingaway.aggregate(Sum('score_away'))
        againstawayscores = partidostandingaway.aggregate(Sum('score_home'))

        #Se agrega la suma para todos los equipos en sus respectivas listas
        totalhomescoreslist.append(totalhomescores['score_home__sum'])
        againstawayscoreslist.append(againstawayscores['score_home__sum'])
        againsthomescoreslist.append(againsthomescores['score_away__sum'])
        totalawayscoreslist.append(totalawayscores['score_away__sum'])

        #Se filtran los partidos que han sido ganados en casa y se los pone a la lista
        partidosganadoshome = partidostanding.filter(score_home__gt=F('score_away'))
        partidosganadoshomelist.append(partidosganadoshome.count())

        #Se filtra los partidos que han sido ganados en visita y se los pone a lista
        partidosganadosaway = partidostandingaway.filter(score_away__gt=F('score_home'))
        partidosganadosawaylist.append(partidosganadosaway.count())


        #Verifica si el equipo gano, perdio o empato su partido local
       # for otheritem in range(len(partidostanding)):
         #   partidostandingwins = partidostanding.filter(score_home__gt = partidostanding[item].score_away)
          #  print partidostandingwins.count()



           # if partidostanding[otheritem].score_home > partidostanding[otheritem].score_away:
            #    print "won"
             #   #suma los partidos ganados de local y los agrega a la lista


           # elif partidostanding[otheritem].score_home == partidostanding[otheritem].score_away:
            #    print "tie"
          #  elif partidostanding[otheritem].score_home < partidostanding[otheritem].score_away:
           #     print "lost"

        #Verifica si    el partido gano, perdio o empato su partido de visita
        #for otheritem in range(len(partidostandingaway)):
         #   if partidostandingaway[otheritem].score_home < partidostandingaway[otheritem].score_away:
          #      print "won visit"
           # elif partidostandingaway[otheritem].score_home == partidostandingaway[otheritem].score_away:
            #    print "tie visit"
           # elif partidostandingaway[otheritem].score_home > partidostandingaway[otheritem].score_away:
            #    print "lost visit"


        #cuenta el numero de partidos activos que han habido localmente
        partidosjugadoshomelist.append(partidostanding.count())
        # cuenta el numero de partidos activos que han habido como visita
        partidosjugadosawaylist.append(partidostandingaway.count())

        #Para las listas que tengan un valor nulo se cambia el valor nulo a 0
        if totalhomescoreslist[item]== None:
            totalhomescoreslist[item]=0
        if totalawayscoreslist[item] == None:
            totalawayscoreslist[item] = 0
        if againsthomescoreslist[item] == None:
            againsthomescoreslist[item] = 0
        if againstawayscoreslist[item] == None:
            againstawayscoreslist[item] = 0



    partido = Match(fixture_id=dict['fixtures'],home=equipos[0])




    #suma las listas necesarias para sacar el numero total de partidos jugados, el numero total de goles a favor
    #el numero total de goles en contra. Para hacer los goles diferencia resta el nnumero total de goles a favor
    #menos el numero total de goles en contra.
    partidosjugadoslist = map(operator.add,partidosjugadoshomelist,partidosjugadosawaylist)
    totalgoalfavor = map(operator.add, totalhomescoreslist,totalawayscoreslist)
    totalgoalagainst = map(operator.add,againsthomescoreslist,againstawayscoreslist)
    totalgoaldif = map(operator.sub, totalgoalfavor,totalgoalagainst)
    partidosganadoslist = map(operator.add,partidosganadoshomelist,partidosganadosawaylist)

    dict['puntajesvista'] = totalawayscoreslist
    dict['puntajeslocales'] = totalhomescoreslist
    dict['golesafavor'] = totalgoalfavor
    dict['golesencontra'] = totalgoalagainst
    dict['golesdiferencia'] = totalgoaldif
    dict['partidosjugados'] = partidosjugadoslist
    dict['victorias'] = victories
    print "papaya"

    print partidosganadoslist



    return render_to_response('standings.html',
            dict)