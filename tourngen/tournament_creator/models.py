from django.db import models

# Create your models here.

class Tournament (models.Model):
	Name = models.CharField(max_length=30)
	Date_Start = models.DateTimeField()
	Date_End = models.DateTimeField()
	Home_or_away = models.BooleanField()
	Info = models.TextField()
	Last_updated = models.DateTimeField()
	Status = models.BooleanField()
	Public = models.BooleanField()

	
