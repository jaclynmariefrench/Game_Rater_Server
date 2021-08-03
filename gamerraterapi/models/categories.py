from django.db import models

class Categories(models.Model):
    """Categories table.
    """
    label = models.CharField(max_length=50)