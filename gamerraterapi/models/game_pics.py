from django.db import models

class GamePics(models.Model):
    """Join model for Game and Players
    """
    player = models.ForeignKey("Players", on_delete=models.CASCADE)
    game = models.ForeignKey("Games", on_delete=models.CASCADE)
    upload_picture = models.URLField()