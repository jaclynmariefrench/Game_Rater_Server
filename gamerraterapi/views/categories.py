"""View module for handling requests about Categories"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from gamerraterapi.models import Categories




class CategoriesView(ViewSet):
    """Game Rater Categories"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single Categories

        Returns:
            Response -- JSON serialized Categories
        """
        try:
            categories = Categories.objects.get(pk=pk)
            serializer = CategoriesSerializer(categories, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all Categoriess

        Returns:
            Response -- JSON serialized list of Categoriess
        """
        categories = Categories.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = CategoriesSerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)

class CategoriesSerializer(serializers.ModelSerializer):
    """JSON serializer for Categories

    Arguments:
        serializers
    """
    class Meta:
        model = Categories
        fields = ('id', 'label')