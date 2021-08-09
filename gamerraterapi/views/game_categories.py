"""View module for handling requests about game Categories"""
from gamerraterapi.models.game_categories import GameCategories
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers




class GameCategoriesView(ViewSet):
    """Level up game Categories"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game Categories

        Returns:
            Response -- JSON serialized game Categories
        """
        try:
            categories = GameCategories.objects.get(pk=pk)
            serializer = GameCategoriesSerializer(categories, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all game Categoriess

        Returns:
            Response -- JSON serialized list of game Categoriess
        """
        categories = GameCategories.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = GameCategoriesSerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)

class GameCategoriesSerializer(serializers.ModelSerializer):
    """JSON serializer for game Categories

    Arguments:
        serializers
    """
    class Meta:
        model = GameCategories
        fields = ('id', 'game', 'category')