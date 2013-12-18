from django import forms
from tournament_creator.models import Fixture
import datetime
from django.forms.extras.widgets import SelectDateWidget
from django.forms import ModelForm, Form

class FixtureForm(forms.ModelForm):

	class Meta:
		model = Fixture
		fields = ('tournament','number','info')
		
