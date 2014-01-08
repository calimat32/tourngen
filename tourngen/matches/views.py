
from django.shortcuts import render, render_to_response
from tournament_creator.models import Team, Tournament, Fixture, Match

# Create your views here.
def listado(request):
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

    return render_to_response('matchviewer.html',dict)