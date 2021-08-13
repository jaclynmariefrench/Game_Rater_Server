from gamerraterapi.views.gameratings import RatingView
from gamerraterapi.views.gamereview import ReviewView
from gamerraterapi.views.game_categories import GameCategoriesView
from gamerraterapi.views.auth import login_user, register_user
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from django.contrib import admin
from gamerraterapi.views import GameView
from gamerraterapi.views import CategoriesView



router = routers.DefaultRouter(trailing_slash=False)
router.register(r'games', GameView, 'game')
router.register(r'gamecategories', GameCategoriesView, 'gamecategory')
router.register(r'categories', CategoriesView, 'category')
router.register(r'gamereviews', ReviewView, 'review')
router.register(r'gameratings', RatingView, 'rating')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
