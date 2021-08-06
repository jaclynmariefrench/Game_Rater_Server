from django.contrib import admin
from gamerraterapi.models import Categories, GameCategories, GamePics, GameRatings, GameReviews, Games, Players

# Register your models here.
admin.site.register(Categories)
admin.site.register(GameCategories)
admin.site.register(GamePics)
admin.site.register(GameRatings)
admin.site.register(GameReviews)
admin.site.register(Games)
admin.site.register(Players)