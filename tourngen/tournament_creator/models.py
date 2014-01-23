# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

from datetime import datetime

class Fixture(models.Model):
    fixture_id = models.AutoField(db_column='Fixture_id', primary_key=True) # Field name made lowercase.
    tournament = models.ForeignKey('Tournament', db_column='Tournament_id') # Field name made lowercase.
    number = models.IntegerField(db_column='Number') # Field name made lowercase.
    info = models.TextField(db_column='Info', blank=True) # Field name made lowercase.
    last_updated = models.DateTimeField(db_column='Last_updated',default=datetime.now) # Field name made lowercase.
    Active = models.BooleanField(db_column='Status',default='true') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'Fixture'

class Match(models.Model):
    match_id = models.AutoField(db_column='Match_id', primary_key=True) # Field name made lowercase.
    fixture = models.ForeignKey(Fixture, db_column='Fixture_id') # Field name made lowercase.
    home = models.ForeignKey('Team', db_column='Home_id', related_name='match_home') # Field name made lowercase.
    away = models.ForeignKey('Team', db_column='Away_id') # Field name made lowercase.
    date = models.DateTimeField(db_column='Date', blank=True, null=True) # Field name made lowercase.
    info = models.TextField(db_column='Info', blank=True) # Field name made lowercase.
    last_updated = models.DateTimeField(db_column='Last_updated',default=datetime.now) # Field name made lowercase.
    active = models.BooleanField(db_column='Status', default='true') # Field name made lowercase.
    score_home = models.IntegerField(db_column='Score_home') # Field name made lowercase.
    score_away = models.IntegerField(db_column='Score_away') # Field name made lowercase.
    played = models.BooleanField(db_column='Played', default='false') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'Match'

class Privilege(models.Model):
    privilege_id = models.IntegerField(db_column='Privilege_id', primary_key=True) # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=80) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'Privilege'

class Team(models.Model):
    team_id = models.AutoField(db_column='Team_id', primary_key=True) # Field name made lowercase.
    tournament = models.ForeignKey('Tournament', db_column='Tournament_id') # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=60) # Field name made lowercase.
    e_mail = models.CharField(db_column='E-mail', max_length=45, blank=True) # Field name made lowercase. Field renamed to remove unsuitable characters.
    info = models.TextField(db_column='Info', blank=True) # Field name made lowercase.
    last_updated = models.DateTimeField(db_column='Last_updated',default=datetime.now) # Field name made lowercase.
    active = models.BooleanField(db_column='Status',default='true') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'Team'
    def __unicode__(self):
	return self.name

class Tournament(models.Model):
    tournament_id = models.AutoField(db_column='Tournament_id', primary_key=True) # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50) # Field name made lowercase.
    date_start = models.DateTimeField(db_column='Date_start') # Field name made lowercase.
    date_end = models.DateTimeField(db_column='Date_end', blank=True, null=True) # Field name made lowercase.
    home_and_away = models.BooleanField(db_column='Home_and_away') # Field name made lowercase.
    info = models.TextField(db_column='Info', blank=True) # Field name made lowercase.
    last_updated = models.DateTimeField(db_column='Last_updated',default=datetime.now) # Field name made lowercase.
    active = models.BooleanField(db_column='Status',default='True') # Field name made lowercase.
    public = models.BooleanField(db_column='Public',default='True') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'Tournament'
        permissions = (
            ("view_tournament", "Can view a tournament"),
        )


    def __unicode__(self):
	return self.name

class TournamentRights(models.Model):
    tournament = models.ForeignKey(Tournament, db_column='Tournament_id') # Field name made lowercase.
    user = models.ForeignKey('User', db_column='User_id') # Field name made lowercase.
    privilege = models.ForeignKey(Privilege, db_column='Privilege_id') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'Tournament_Rights'

class User(models.Model):
    user_id = models.IntegerField(db_column='User_id', primary_key=True) # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=60) # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=60) # Field name made lowercase.
    e_mail = models.CharField(db_column='E-mail', max_length=100) # Field name made lowercase. Field renamed to remove unsuitable characters.
    birthday = models.DateTimeField(db_column='Birthday', blank=True, null=True) # Field name made lowercase.
    status = models.IntegerField(db_column='Status') # Field name made lowercase.
    last_updated = models.DateTimeField(db_column='Last_updated') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'User'

class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=80)
    class Meta:
        managed = False
        db_table = 'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')
    class Meta:
        managed = False
        db_table = 'auth_group_permissions'

class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'auth_permission'

class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'auth_user'

class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)
    class Meta:
        managed = False
        db_table = 'auth_user_groups'

class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)
    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'

class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    user = models.ForeignKey(AuthUser)
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.IntegerField()
    change_message = models.TextField()
    class Meta:
        managed = False
        db_table = 'django_admin_log'

class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'django_content_type'

class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'django_session'

