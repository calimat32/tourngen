from django import forms
from tournament_creator.models import Team
import datetime
from django.forms.extras.widgets import SelectDateWidget
from django.forms import ModelForm, Form

class TeamForm(forms.ModelForm):

	class Meta:
		model = Team
		fields = ('tournament','name','e_mail','info')
