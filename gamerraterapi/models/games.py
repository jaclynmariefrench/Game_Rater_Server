from django.db import models
from django.db.models.fields import DateField, FloatField, IntegerField

class Games(models.Model):
    """Games Table.
    """
    title = models.CharField(max_length=500)
    designer = models.CharField(max_length=500)
    year_released = DateField()
    number_of_players = IntegerField()
    time_to_play = FloatField()
    age_recommendation = IntegerField()