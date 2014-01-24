from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView , FormView, CreateView
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
from guardian.shortcuts import assign_perm, get_objects_for_user , get_perms
from django.db.models import Q
import pprint





# Create your views here.
#Clase que permite registrar a un usuario y asignarle permisos
class Registrarse(FormView):
    template_name = 'registration/registrarse.html'
    form_class = UserForm
    success_url = reverse_lazy('register')

    def form_valid(self,form):
        addtournament = Permission.objects.get(codename='add_tournament')
        changematch = Permission.objects.get(codename='change_match')
        addmatch = Permission.objects.get(codename='add_match')
        add_dataentry_user = Permission.objects.get(codename='add_dataentry')
        addteam = Permission.objects.get(codename='add_team')

        user = form.save()
        user.user_permissions.add(addtournament)
        user.user_permissions.add(changematch)
        user.user_permissions.add(add_dataentry_user)
        user.user_permissions.add(addteam)
        user.user_permissions.add(addmatch)

        return super(Registrarse,self).form_valid(form)

#Agrega usuarios digitadores con un solo permiso para que depsues puedan ser agergados a los torneos que se necesiten

class RegistrarDigitador(CreateView):
    success_url = reverse_lazy('register_dataentry')
    template_name = 'registration/registrardigitador.html'
    form_class = UserForm


    def form_valid(self,form):
        #addtournament = Permission.objects.get(codename='add_tournament')
        #changematch = Permission.objects.get(codename='change_match')
        #add_dataentry_user = Permission.objects.get(codename='add_dataentry')
        data_entry = Permission.objects.get(codename='usario_digitador')

        user = form.save()
        #user.user_permissions.add(addtournament)
        user.user_permissions.add(data_entry)
        #user.user_permissions.add(add_dataentry_user)

        return super(RegistrarDigitador,self).form_valid(form)

#Funcion que permite agregar permisos a todos los usuarios que sean digitadores,
#se ele entrega un torneo al usuario y este podra luego editarlo cuando inicie sesion
@permission_required('tournament_creator.add_dataentry')
def AsignarPermisos(request):
    dict = {}
    dict['tournaments'] = get_objects_for_user(request.user,'tournament_creator.view_tournament')
    perm = Permission.objects.get(codename='usario_digitador')
    users = User.objects.filter(Q(groups__permissions=perm) | Q(user_permissions=perm) ).distinct()
    dict['users'] = users
    #idtorneo = request.GET.get('tournament')
    #idusuario = request.GET.get('usuario')
    #usuario_seleccionado = User.objects.get(id=idusuario)
    #torne_seleccionado = Tournament.objects.get(tournament_id=idtorneo)
    #pprint.pprint(usuario_seleccionado)
    #assign_perm('usuario_digitador',usuario_seleccionado,torne_seleccionado)
    pprint.pprint(users)
    return render_to_response('asignarpermisosdigitador.html',dict)

@permission_required('tournament_creator.add_dataentry')
def SuccessPermission(request):
    idtorneo = request.GET.get('tournament')
    idusuario = request.GET.get('usuario')
    usuario_seleccionado = User.objects.get(id=idusuario)
    torneo_seleccionado = Tournament.objects.get(tournament_id=idtorneo)
    pprint.pprint(torneo_seleccionado)
    changematch = Permission.objects.get(codename='change_match')
    assign_perm('view_tournament',usuario_seleccionado,torneo_seleccionado)
    usuario_seleccionado.user_permissions.add(changematch)
    return render_to_response('permissionsuccess.html')






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
