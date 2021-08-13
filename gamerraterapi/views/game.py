"""View module for handling requests about games"""
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



class GameView(ViewSet):
    """Game Rater"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """

        # Uses the token passed in the `Authorization` header
        player = Players.objects.get(user=request.auth.user)

        game = Games()
        game.title = request.data["title"]
        game.designer = request.data["designer"]
        game.number_of_players = request.data["number_of_players"]
        game.time_to_play = request.data["time_to_play"]
        game.player = player
        game.year_released = request.data["year_released"]
        game.age_recommendation = request.data["age_recommendation"]

        categories = GameCategories.objects.get(pk=request.data["categories"])

        # Try to save the new game to the database, then
        # serialize the game instance as JSON, and send the
        # JSON as a response to the client request
        try:
            game.save()
            game.categories.set([categories])
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data) 

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/games/2
            #
            # The `2` at the end of the route becomes `pk`
            game = Games.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        player = Players.objects.get(user=request.auth.user)

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Game, get the game record
        # from the database whose primary key is `pk`
        game = Games()
        game.title = request.data["title"]
        game.designer = request.data["designer"]
        game.number_of_players = request.data["number_of_players"]
        game.time_to_play = request.data["time_to_play"]
        game.player = player
        game.year_released = request.data["year_released"]
        game.age_recommendation = request.data["age_recommendation"]

        categories = GameCategories.objects.get(pk=request.data["categories"])
        game.categories = categories
        game.save()

        # CODE FROM HANNAH vvvvv
        serializer = GameSerializer(game, context= {'request': request})

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        # CODE FROM CHAPTER vvvv
        # return Response({}, status=status.HTTP_204_NO_CONTENT)

        # CODE FROM HANNAH vvvvvv
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            game = Games.objects.get(pk=pk)
            game.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Games.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of games
        """
        # Get all game records from the database
        games = Games.objects.all()

        # Support filtering games by category
        #    http://localhost:8000/games?category=1
        #
        # That URL will retrieve all tabletop games
        categories = self.request.query_params.get('categories', None)
        if categories is not None:
            games = games.filter(categories__id=categories)

        serializer = GameSerializer(
            games, many=True, context={'request': request})
        return Response(serializer.data)


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games

    Arguments:
        serializer category
    """
    class Meta:
        model = Games
        fields = ('id', 'title', 'designer', 'year_released', 'number_of_players', 'time_to_play', 'age_recommendation', 'categories', 'average_rating')
        depth = 1

