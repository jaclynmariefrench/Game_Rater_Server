from django.db import models

class GameCategories(models.Model):
    """Join table for games and categories.
    """
    category = models.ForeignKey("Categories", on_delete=models.CASCADE)
    game = models.ForeignKey("Games", on_delete=models.CASCADE)