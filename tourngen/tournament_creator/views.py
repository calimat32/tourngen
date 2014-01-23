from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView , FormView
from django.template import RequestContext
from forms import TournamentForm
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse_lazy
from tournament_creator.models import Tournament, Match
from tournament_creator.models import Team
from tournament_creator.forms import UserForm
from userroles.models import set_user_role
from userroles import roles
from django.contrib.auth.models import User
from rbac.models import RBACRole
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import permission_required
from guardian.shortcuts import assign_perm, get_objects_for_user






# Create your views here.

class Registrarse(FormView):
    template_name = 'registration/registrarse.html'
    form_class = UserForm
    success_url = reverse_lazy('register')

    def form_valid(self,form):
        permission = Permission.objects.get(codename='add_tournament')

        user = form.save()
        user.user_permissions.add(permission)

        return super(Registrarse,self).form_valid(form)



class Usuario(TemplateView):
    def get(self, request, *args, **kwargs):
        usuario = request.user
        print
        usuario
        dic = {'usuario': usuario}
        return render_to_response('startup/usuario.html', dic)


def tournaments(request):
    tournament = Tournament.objects.all().filter(active='true')
    permission = Permission.objects.filter(codename='view_tournament')
    return render_to_response('tournaments.html',
                              {'tournaments': get_objects_for_user(request.user,'tournament_creator.view_tournament')})


def tournament(request, tournament_id=1):
    return render_to_response('tournament.html', {'tournament': Tournament.objects.get(tournament_id=tournament_id)
    })

@permission_required('tournament_creator.add_tournament')
def create(request):
    if request.POST:
        form = TournamentForm(request.POST)
        if form.is_valid():
            tournament = form.save()
            #permission = Permission.objects.get(codename='change_tournament')
            user = request.user
            assign_perm('view_tournament', user, tournament)

            return HttpResponseRedirect('/tournament/all')
    else:
        form = TournamentForm()
    args = {}
    args.update(csrf(request))

    args['form'] = form

    return render_to_response('create_tournament.html', args)
