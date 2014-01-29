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
        delete_tourn = Permission.objects.get(codename='delete_tournament')
        changematch = Permission.objects.get(codename='change_match')
        addmatch = Permission.objects.get(codename='add_match')
        add_dataentry_user = Permission.objects.get(codename='add_dataentry')
        add_representative = Permission.objects.get(codename='usuario_rep')
        addteam = Permission.objects.get(codename='add_team')
        delete_team = Permission.objects.get(codename='delete_team')

        user = form.save()
        user.user_permissions.add(addtournament)
        user.user_permissions.add(changematch)
        user.user_permissions.add(add_dataentry_user)
        user.user_permissions.add(addteam)
        user.user_permissions.add(addmatch)
        user.user_permissions.add(add_representative)
        user.user_permissions.add(delete_tourn)
        user.user_permissions.add(delete_team)

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

#Funcion que crea usuario representante de equipo con un permiso asignado para diferenciar despues que es representante de equipo
class RegistrarRepresentante(CreateView):
    success_url = reverse_lazy('register_rep')
    template_name = 'registration/registrardigitador.html'
    form_class = UserForm


    def form_valid(self,form):
        #addtournament = Permission.objects.get(codename='add_tournament')
        #changematch = Permission.objects.get(codename='change_match')
        #add_dataentry_user = Permission.objects.get(codename='add_dataentry')
        add_representative = Permission.objects.get(codename='is_rep')

        user = form.save()
        #user.user_permissions.add(addtournament)
        user.user_permissions.add(add_representative)
        #user.user_permissions.add(add_dataentry_user)

        return super(RegistrarRepresentante,self).form_valid(form)

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
    #pprint.pprint(users)
    return render_to_response('asignarpermisosdigitador.html',dict)

#Vista del permiso que se muestra cuando se asignaron los permisos con exito
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


#Vista para asignar los permisos al usuario representante de equipo
@permission_required('tournament_creator.usuario_rep')
def AsignarPermisosRep(request):
    dict = {}
    dict['teams'] = get_objects_for_user(request.user,'tournament_creator.view_team')
    perm = Permission.objects.get(codename='is_rep')
    users = User.objects.filter(Q(groups__permissions=perm) | Q(user_permissions=perm) ).distinct()
    dict['users'] = users
    #idtorneo = request.GET.get('tournament')
    #idusuario = request.GET.get('usuario')
    #usuario_seleccionado = User.objects.get(id=idusuario)
    #torne_seleccionado = Tournament.objects.get(tournament_id=idtorneo)
    #pprint.pprint(usuario_seleccionado)
    #assign_perm('usuario_digitador',usuario_seleccionado,torne_seleccionado)
    #pprint.pprint(users)
    return render_to_response('asignarpermisosrep.html',dict)

#Vista de permisos fueron asignados correctamente para usuario representante
@permission_required('tournament_creator.usuario_rep')
def SuccessPermissionRep(request):
    idtorneo = request.GET.get('tournament')
    idusuario = request.GET.get('usuario')
    usuario_seleccionado = User.objects.get(id=idusuario)
    torneo_seleccionado = Tournament.objects.get(tournament_id=idtorneo)
    pprint.pprint(torneo_seleccionado)
    #changematch = Permission.objects.get(codename='change_match')
    assign_perm('view_tournament',usuario_seleccionado,torneo_seleccionado)
    #usuario_seleccionado.user_permissions.add(changematch)
    return render_to_response('permissionsuccess.html')



class Usuario(TemplateView):
    def get(self, request, *args, **kwargs):
        usuario = request.user
        print
        usuario
        dic = {'usuario': usuario}
        return render_to_response('startup/usuario.html', dic)

@permission_required('tournament_creator.delete_tournament')
def tournaments(request):
    tournament = Tournament.objects.all().filter(active='true')
    permission = Permission.objects.filter(codename='view_tournament')
    return render_to_response('tournaments.html',
                              {'tournaments': get_objects_for_user(request.user,'tournament_creator.view_tournament')})

@permission_required('tournament_creator.delete_tournament')
def tournament(request, tournament_id=1):
    return render_to_response('tournament.html', {'tournament': Tournament.objects.get(tournament_id=tournament_id)
    })

@permission_required('tournament_creator.delete_tournament')
def deletetournament(request):
    dict = {}
    idtorneo = request.GET.get('torneos')
    tournament = Tournament.objects.get(tournament_id = idtorneo)
    pprint.pprint(tournament)
    tournament.delete()
    return render_to_response('deletetournament.html',dict)

@permission_required('tournament_creator.add_tournament')
def create(request):
    if request.POST:
        form = TournamentForm(request.POST)
        if form.is_valid():
            tournament = form.save()
            #permission = Permission.objects.get(codename='change_tournament')
            user = request.user
            assign_perm('view_tournament', user, tournament)

            return HttpResponseRedirect('/team/create')
    else:
        form = TournamentForm()
    args = {}
    args.update(csrf(request))

    args['form'] = form

    return render_to_response('create_tournament.html', args)
