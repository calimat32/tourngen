from django.shortcuts import render
from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView
from django.template import RequestContext
from forms import TeamForm
from django.http import HttpResponseRedirect 
from django.core.context_processors import csrf 
from tournament_creator.models import Team


# Create your views here.

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
				{'teams': Team.objects.all()})

def team(request,team_id=1):
	return render_to_response('team.html', {'team':Team.objects.get(team_id=team_id) })
