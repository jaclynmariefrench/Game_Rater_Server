from django.db import models

class GameReviews(models.Model):
    """Join model for Game and Players for reviewing the game.
    """
    player = models.ForeignKey("Players", on_delete=models.CASCADE)
    game = models.ForeignKey("Games", on_delete=models.CASCADE)
    review = models.CharField(max_length=500)