from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView
from django.template import RequestContext
# Create your views here.

class Usuario(TemplateView):
	def get(self, request, *args, **kwargs):
		return render_to_response('startup/usuario.html')

