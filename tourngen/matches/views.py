from django.shortcuts import render, render_to_response
from tournament_creator.models import Team, Tournament, Fixture, Match
from matches.models import Standing
from django.db.models import Sum, Count, F
from guardian.shortcuts import assign_perm, get_objects_for_user
from django.contrib.auth.decorators import permission_required
import operator
import pprint
import itertools


# Create your views here.

estado = True

#Funcion para editar los partidos 
def editarpartidos(id, scorehome, scoreaway,jorn):
    partido = Match.objects.get(match_id=id)
    partido.score_home = scorehome
    partido.score_away = scoreaway
    partido.played = 1
    partido.fixture_id = jorn
    partido.active = False
    partido.save()

#Funcion para insertar un partido
def insertarpartido(jorn,elocal,evisita):
    partido = Match()
    partido.fixture_id = jorn
    partido.home = elocal
    partido.away = evisita
    partido.score_home = 0
    partido.score_away = 0
    partido.played = False
    partido.save()


#Muestra el listado de todos los partidos creados
@permission_required('tournament_creator.change_match')
def listado(request):
    #Obtiene los valores obtenidos por el request a traves del metodo get
    idpartido = request.GET.get('partido_id')
    puntajelocal = request.GET.get('score_local')
    puntajevisita = request.GET.get('score_visita')

    #editarpartidos(idpartido,puntajelocal,puntajevisita)


    dict = {'partidos': Match.objects.filter(played="true"),
            #muestra los torneos que el usuario tiene
            'tournaments': get_objects_for_user(request.user, 'tournament_creator.view_tournament')}

    return render_to_response('matchviewer.html', dict)

#Vista que muestra los partidos para cambairles el fixture
def listadofixture(request):
    #Obtiene los valores obtenidos por el request a traves del metodo get
    idpartido = request.GET.get('partido_id')
    puntajelocal = request.GET.get('score_local')
    puntajevisita = request.GET.get('score_visita')

    #editarpartidos(idpartido,puntajelocal,puntajevisita)


    dict = {'partidos': Match.objects.filter(played="true"),
            #muestra los torneos que el usuario tiene
            'tournaments': get_objects_for_user(request.user, 'tournament_creator.view_tournament')}

    return render_to_response('matchviewerupdate.html', dict)




#Muestra los todoso los torneos que se han mostrado como publicos para genera los standings
def listadovisita(request):
    listado(request)
    dict = {}
    dict['tournaments'] = Tournament.objects.filter(public=True, active=True)
    return render_to_response('listadovisita.html',dict)

#Vista para mostrar el listado de los partidos asignados al equipo representante
def listadorep(request):
    dict = {}
    tournament = get_objects_for_user(request.user,'tournament_creator.view_tournament')

    dict['tournaments'] = tournament
    return render_to_response('listadorep.html',dict)


#Muestra el template cuando un partido fue guardado los goles exitosamente.
@permission_required('tournament_creator.change_match')
def success(request):
    idpartido = request.GET.get('partido_id')
    puntajelocal = request.GET.get('score_local')
    puntajevisita = request.GET.get('score_visita')
    #fecha = request.GET.get('fecha_partido')
    jorn1 = request.GET.get('jornada')
    #Obtiene el partido de la id al cual el usuario cambia y despues actualiza sus puntajes,
    #despues lo guarda en la base de datos.





    dict = {'partidos': Match.objects.all(),
            'tournaments': Tournament.objects.filter(active="true")}



    editarpartidos(idpartido, puntajelocal, puntajevisita,jorn1)




    return render_to_response('matchsuccess.html', dict)

#Muestra el template cuando un partido fue insertado exitosamente
def successact(request):

    equipolocalid = request.GET.get('equipolocal')
    equipovisitaid = request.GET.get('equipovisita')
    teamlocal = Team.objects.get(team_id=equipolocalid)
    teamvisita = Team.objects.get(team_id=equipovisitaid)
    jorn1 = request.GET.get('jornada')
    #Obtiene el partido de la id al cual el usuario cambia y despues actualiza sus puntajes,
    #despues lo guarda en la base de datos.
    pprint.pprint(teamvisita)

    #editarpartidos(idpartido, puntajelocal, puntajevisita,jorn1)
    dict = {'partidos': Match.objects.all(),
            'tournaments': Tournament.objects.filter(active="true")}

    if (equipolocalid != equipovisitaid):
        insertarpartido(jorn1,teamlocal,teamvisita)
        dict['mensaje'] = "Tu partido fue insertado correctamente"
    else:
        dict['mensaje'] = "No se puede agregar un partido con el mismo equipo de local y visita"

    return render_to_response('matchsuccessact.html', dict)


#Filtra los torneos del los torneos publicos para el usuario visita
def filterguestmatches(request):
    myrequest = "salsa"
    torneosfiltrados = request.GET.get('torneos')
    dict = {'tournaments': Tournament.objects.filter(active="true"),
            'numberofteams': Team.objects.filter(tournament_id=request.get_full_path()[-1:]).count(),
            'teams': Team.objects.filter(tournament_id=torneosfiltrados),
            'fixtures': Fixture.objects.filter(tournament_id=torneosfiltrados),
            'unito': myrequest,
            'selected_tournament': Tournament.objects.get(tournament_id=torneosfiltrados),

            'tournid': request.get_full_path()[-1:]}

    equipos = Team.objects.filter(tournament_id=torneosfiltrados)
    dict['partidos'] = Match.objects.filter(fixture_id=dict['fixtures'],active=True)

    return render_to_response('filterguestmatch.html',
                              dict)

def filtermymatches(request):
    myrequest = "salsa"
    torneosfiltrados = request.GET.get('torneos')
    dict = {'tournaments': Tournament.objects.filter(active="true"),
            'numberofteams': Team.objects.filter(tournament_id=torneosfiltrados).count(),
            'teams': Team.objects.filter(tournament_id=torneosfiltrados),
            'fixtures': Fixture.objects.filter(tournament_id=torneosfiltrados),
            'unito': myrequest,
            'selected_tournament': Tournament.objects.get(tournament_id=torneosfiltrados),

            'tournid': torneosfiltrados}

    equipos = Team.objects.filter(tournament_id=torneosfiltrados)
    dict['partidos'] = Match.objects.filter(fixture_id=dict['fixtures'],active=True)

    return render_to_response('filterguestmatch.html',
                              dict)


#Filtra los partidos dependendo del torneo al cual se le es asignado
def filtermatches(request):
    myrequest = "salsa"
    torneosfiltrados = request.GET.get('torneos')
    dict = {'tournaments': Tournament.objects.filter(active="true"),
            'numberofteams': Team.objects.filter(tournament_id=torneosfiltrados).count(),
            'teams': Team.objects.filter(tournament_id=torneosfiltrados),
            'fixtures': Fixture.objects.filter(tournament_id=torneosfiltrados),
            'unito': myrequest,
            'selected_tournament': Tournament.objects.get(tournament_id=torneosfiltrados),

            'tournid': torneosfiltrados}

    equipos = Team.objects.filter(tournament_id=torneosfiltrados)
    dict['partidos'] = Match.objects.filter(fixture_id=dict['fixtures'],active=True)


    return render_to_response('filtermatch.html',
                              dict)

#Vista para los partidos filtrados para actualizar los fixture
def filtermatchesact(request):
    myrequest = "salsa"
    torneosfiltrados = request.GET.get('torneos')
    dict = {'tournaments': Tournament.objects.filter(active="true"),
            'numberofteams': Team.objects.filter(tournament_id=torneosfiltrados).count(),
            'teams': Team.objects.filter(tournament_id=torneosfiltrados),
            'fixtures': Fixture.objects.filter(tournament_id=torneosfiltrados),
            'unito': myrequest,
            'selected_tournament': Tournament.objects.get(tournament_id=torneosfiltrados),

            'tournid': torneosfiltrados}

    equipos = Team.objects.filter(tournament_id=torneosfiltrados)
    dict['partidos'] = Match.objects.filter(fixture_id=dict['fixtures'])


    return render_to_response('filtermatchact.html',
                              dict)


#Funcion que permite cambiar las entradas vacias de las listas a 0
def changeNone(lista, index):
    if lista[index] == None:
        lista[index] = 0


#Crea la tabla de posiciones
def createstandings(request):
    myrequest = "salsa"
    torneosfiltrados = request.GET.get('torneos')
    dict = {'tournaments': Tournament.objects.filter(active="true"),
            'teams': Team.objects.filter(tournament_id=torneosfiltrados),
            'fixtures': Fixture.objects.filter(tournament_id=torneosfiltrados),
            'unito': myrequest,
            'selected_tournament': Tournament.objects.get(tournament_id=torneosfiltrados)}

    equipos = Team.objects.filter(tournament_id=torneosfiltrados)
    dict['partidos'] = Match.objects.filter(fixture_id=dict['fixtures'])

    #Declaacion de variables que seran usadas despues
    victories = list()
    partidosjugadoshomelist = list()
    partidosjugadosawaylist = list()
    partidosganadoslist = list()
    partidosperdidoslist = list()
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
    partidosperdidoshomelist = list()
    partidosperdidosawaylist = list()
    partidosempatadoshomelist = list()
    partidosempatadosawaylist = list()
    partidosempatadoslist = list()
    dummy = 0
    partidosganadoshome = 0
    partidosjugadoshome = 0
    partidosjugadosaway = 0
    partidosjugadoslist = list()
    standinglist = list()

    for item in range(len(equipos)):
        #Saca los goles a favor y los goles en contra, partidostanding son todos los partidos que tengan a cada equipo
        #como equipo local y partidostandingaway son todos los partidos que tengan a cada equipo como equipo visita.
        partidostanding = Match.objects.filter(fixture_id=dict['fixtures'], home=equipos[item].team_id, played="true")
        partidostandingaway = Match.objects.filter(fixture_id=dict['fixtures'], away=equipos[item].team_id,
                                                   played="true")

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

        #Se filtran los partidos que han sido perdidos en casa y se los pone en la lista
        partidosperdidoshome = partidostanding.filter(score_away__gt=F('score_home'))
        partidosperdidoshomelist.append(partidosperdidoshome.count())

        #Se filtra los partidos que han sido ganados en visita y se los pone a lista
        partidosganadosaway = partidostandingaway.filter(score_away__gt=F('score_home'))
        partidosganadosawaylist.append(partidosganadosaway.count())

        #Se filtra los partidos que se han perdido en visita y se los pone a la lista
        partidosperdidosaway = partidostandingaway.filter(score_home__gt=F('score_away'))
        partidosperdidosawaylist.append(partidosperdidosaway.count())

        #se filtra los partidos que se han empatado
        partidosempatadoshome = partidostanding.filter(score_home__exact=F('score_away'))
        partidosempatadoshomelist.append(partidosempatadoshome.count())
        partidosempatadosaway = partidostandingaway.filter(score_home__exact=F('score_away'))
        partidosempatadosawaylist.append(partidosempatadosaway.count())


        #se crea un diccionario para cada equipo y poder mandarlo al template
        equipodictionary = {'partidosjugados': partidostanding.count() + partidostandingaway.count(),
                            'partidosganados': partidosganadoshome.count() + partidosganadosaway.count(),
                            'partidosperdidos': partidosperdidoshome.count() + partidosperdidosaway.count(),
                            'partidosempatados': partidosempatadoshome.count() + partidosempatadosaway.count()


        }



        # equipodictionary['golesdiferencia'] = equipodictionary['golesafavor']-equipodictionary['goleencontra']
        equipodictionary['puntos'] = equipodictionary['partidosganados'] * 3 + equipodictionary['partidosempatados']

        #cuenta el numero de partidos activos que han habido localmente
        partidosjugadoshomelist.append(partidostanding.count())
        # cuenta el numero de partidos activos que han habido como visita
        partidosjugadosawaylist.append(partidostandingaway.count())

        #Para las listas que tengan un valor nulo se cambia el valor nulo a 0
        changeNone(totalhomescoreslist, item)
        changeNone(totalawayscoreslist, item)
        changeNone(againsthomescoreslist, item)
        changeNone(againstawayscoreslist, item)


        #otros valores se agregan al diccionario despues de arreglar las listas
        equipodictionary['golesafavor'] = totalhomescoreslist[item] + totalawayscoreslist[item]
        equipodictionary['golesencontra'] = againstawayscoreslist[item] + againsthomescoreslist[item]
        equipodictionary['golesdiferencia'] = equipodictionary['golesafavor'] - equipodictionary['golesencontra']
        equipodictionary['puntos'] = equipodictionary['partidosganados'] * 3 + equipodictionary['partidosempatados']
        equipodictionary['teams'] = equipos[item]


        #Se agregan todos los diccionarios de los equipos a una lista
        standinglist.append(equipodictionary)





    #Se ordena la lista de diccionarios para poder mostrarlos ordenados en el template.
    standingorderlist = sorted(standinglist, key=lambda item: (item['puntos'], item['golesdiferencia']), reverse=True)



    #se agrega el la lista al diccionario que se va a renderizar en el template
    dict['posiciones'] = standingorderlist

    return render_to_response('standings.html',
                              dict)
