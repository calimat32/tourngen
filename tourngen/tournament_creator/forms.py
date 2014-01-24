from django import forms
from models import Tournament, AuthUser
import datetime
from django.forms.extras.widgets import SelectDateWidget
from django.forms import ModelForm, Form
from django.contrib.auth.forms import UserCreationForm



class UserForm(UserCreationForm):
    pass


class TournamentForm(forms.ModelForm):
	
	class Meta:
		model = Tournament 
		fields = 	 ( 'name','date_start','date_end','home_and_away','info','public')


