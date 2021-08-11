"""View module for handling requests about reviews"""
from django.db.models.fields.related import ForeignKey
from gamerraterapi.models.game_reviews import GameReviews
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



class ReviewView(ViewSet):
    """Game Rater ratings"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized review instance
        """

        # Uses the token passed in the `Authorization` header

        review = GameReviews()
        review.review = request.data["review"]

        game = Games.objects.get(id=request.data["game"])
        player = Players.objects.get(id=request.data["player"])

        # Try to save the new game to the database, then
        # serialize the game instance as JSON, and send the
        # JSON as a response to the client request
        try:
            review.save()
            review.game.set([game])
            review.player.set([player])
            serializer = ReviewSerializer(review, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single review

        Returns:
            Response -- JSON serialized review instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/games/2
            #
            # The `2` at the end of the route becomes `pk`
            review = GameReviews.objects.get(pk=pk)
            serializer = ReviewSerializer(review, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a review

        Returns:
            Response -- Empty body with 204 status code
        """
        player = Players.objects.get(user=request.auth.user)

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Game, get the game record
        # from the database whose primary key is `pk`
        review = GameReviews()
        review.review = request.data["review"]

        game = Games.objects.get(pk=request.data["game"])
        review.save()

        # CODE FROM HANNAH vvvvv
        serializer = ReviewSerializer(review, context= {'request': request})

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        # CODE FROM CHAPTER vvvv
        # return Response({}, status=status.HTTP_204_NO_CONTENT)

        # CODE FROM HANNAH vvvvvv
        return Response(serializer.data)
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single review

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            review = GameReviews.objects.get(pk=pk)
            review.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except GameReviews.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to review resource

        Returns:
            Response -- JSON serialized list of reviews
        """
        # Get all review records from the database
        reviews = GameReviews.objects.all()

        player = self.request.query_params.get('players', None)
        game = self.request.query_params.get('games', None)

        serializer = ReviewSerializer(
            reviews, many=True, context={'request': request})
        return Response(serializer.data)


class ReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for reviews

    Arguments:
        serializer category
    """
    class Meta:
        model = GameReviews
        fields = ('id', 'player', 'game', 'review')
        depth = 1
