from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView
from django.template import RequestContext
from forms import TournamentForm
from django.http import HttpResponseRedirect 
from django.core.context_processors import csrf 
from tournament_creator.models import Tournament


# Create your views here.

class Usuario(TemplateView):
	def get(self, request, *args, **kwargs):
		usuario = request.user 
		print usuario
		dic = {'usuario':usuario}
		return render_to_response('startup/usuario.html',dic)

def tournaments(request):
	return render_to_response('tournaments.html',
				{'tournaments': Tournament.objects.all()})

def tournament(request,tournament_id=1):
	return render_to_response('tournament.html', {'tournament':Tournament.objects.get(tournament_id=tournament_id) })
	


def create(request):
	if request.POST:
		form = TournamentForm(request.POST)
		if form.is_valid():
			form.save()
			
			return HttpResponseRedirect('/tournament/all')
	else:
		form = TournamentForm()
	args = {}
	args.update(csrf(request))

	args['form'] = form
	
	return render_to_response('create_tournament.html', args)
