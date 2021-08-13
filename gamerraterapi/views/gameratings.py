"""View module for handling requests about ratings"""
from django.db.models.fields.related import ForeignKey
from gamerraterapi.models.game_ratings import GameRatings
from rest_framework.views import set_rollback
from gamerraterapi.models.game_categories import GameCategories
from gamerraterapi.models.games import Games
from gamerraterapi.models.players import Players
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status



class RatingView(ViewSet):
    """Game Rater ratings"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized rating instance
        """

        # Uses the token passed in the `Authorization` header

        rating = GameRatings()
        rating.rating = request.data["rating"]

        rating.game = Games.objects.get(pk=request.data["game"]) 
        rating.player = Players.objects.get(user=request.auth.user)

        # Try to save the new game to the database, then
        # serialize the game instance as JSON, and send the
        # JSON as a response to the client request
        try:
            rating.save()
            serializer = RatingSerializer(rating, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single rating

        Returns:
            Response -- JSON serialized rating instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/games/2
            #
            # The `2` at the end of the route becomes `pk`
            rating = GameRatings.objects.get(pk=pk)
            serializer = RatingSerializer(rating, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a rating

        Returns:
            Response -- Empty body with 204 status code
        """
        player = Players.objects.get(user=request.auth.user)

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Game, get the game record
        # from the database whose primary key is `pk`
        rating = GameRatings()
        rating.rating = request.data["rating"]

        game = Games.objects.get(pk=request.data["game"])
        rating.save()

        # CODE FROM HANNAH vvvvv
        serializer = RatingSerializer(rating, context= {'request': request})

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        # CODE FROM CHAPTER vvvv
        # return Response({}, status=status.HTTP_204_NO_CONTENT)

        # CODE FROM HANNAH vvvvvv
        return Response(serializer.data)
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single rating

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            rating = GameRatings.objects.get(pk=pk)
            rating.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except GameRatings.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to rating resource

        Returns:
            Response -- JSON serialized list of ratings
        """
        # Support filtering games by id
        #    http://localhost:8000/gameratings?game=1
        
        # That URL will retrieve all tabletop games

        # Get all rating records from the database
        ratings = GameRatings.objects.all()
        
        game = self.request.query_params.get('game', None)
        if game is not None:
            ratings = ratings.filter(game_id=game)
        serializer = RatingSerializer(
            ratings, many=True, context={'request': request})
        return Response(serializer.data)


class RatingSerializer(serializers.ModelSerializer):
    """JSON serializer for ratings

    Arguments:
        serializer category
    """
    class Meta:
        model = GameRatings
        fields = ('id', 'player', 'game', 'rating')
        depth = 1
