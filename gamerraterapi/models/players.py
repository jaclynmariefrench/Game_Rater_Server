from django.db import models
from django.contrib.auth.models import User


class Players(models.Model):
    """Player Model
    Args:
        models (OneToOneField): The user information for the gamer
        bio (CharField): The bio of the user
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=50)