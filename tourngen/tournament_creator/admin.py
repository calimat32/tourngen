from django.contrib import admin
from tournament_creator.models import *

# Register your models here.

admin.site.register(Tournament)
admin.site.register(Team)
admin.site.register(Fixture)
admin.site.register(Match)
