from django.db import models

class GameRatings(models.Model):
    """Join model for Game and Players for rating the game.
    """
    player = models.ForeignKey("Players", on_delete=models.CASCADE)
    game = models.ForeignKey("Games", on_delete=models.CASCADE)
    rating = models.IntegerField()