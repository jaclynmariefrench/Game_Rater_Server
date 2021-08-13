from gamerraterapi.models.game_ratings import GameRatings
from gamerraterapi.models import categories, game_categories, game_reviews
from django.db import models
from django.db.models.fields import DateField, IntegerField, TimeField

class Games(models.Model):
    """Games Table.
    """
    title = models.CharField(max_length=500)
    designer = models.CharField(max_length=500)
    year_released = IntegerField()
    number_of_players = IntegerField()
    time_to_play = IntegerField()
    age_recommendation = IntegerField()
    categories = models.ManyToManyField("Categories", through="GameCategories")

    @property
    def average_rating(self):
        """Average rating calculated attribute for each game"""
        ratings = GameRatings.objects.filter(game=self)

        # Sum all of the ratings for the game
        total_rating = 0
        for rating in ratings:
            total_rating += rating.rating

        # Calculate the averge and return it.
        # If eou don't know how to calculate averge, Google it.
            number_of_ratings = len(ratings)
            total_average_rating = total_rating/number_of_ratings

            return total_average_rating

    @average_rating.setter
    def average_rating(self, value):
        self.__average_rating = value
            
    
    
    
    
    
    
