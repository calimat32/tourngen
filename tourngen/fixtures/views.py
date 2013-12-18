from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView
from django.template import RequestContext
from forms import FixtureForm
from django.http import HttpResponseRedirect 
from django.core.context_processors import csrf 
from tournament_creator.models import Fixture


# Create your views here.

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
				{'fixtures': Fixture.objects.all()})

def fixture(request,fixture_id=1):
	return render_to_response('fixture.html', {'fixture':Fixture.objects.get(fixture_id=fixture_id) })
