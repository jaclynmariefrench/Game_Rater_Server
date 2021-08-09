from gamerraterapi.models import categories, game_categories, game_reviews
from django.db import models
from django.db.models.fields import DateField, IntegerField, TimeField

class Games(models.Model):
    """Games Table.
    """
    title = models.CharField(max_length=500)
    designer = models.CharField(max_length=500)
    year_released = DateField()
    number_of_players = IntegerField()
    time_to_play = IntegerField()
    age_recommendation = IntegerField()
    categories = models.ManyToManyField("Categories", through="GameCategories")
    
    
    
    
    
    
