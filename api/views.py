from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from  rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(id=1)
    serializer_class = UserSerializer
    # authentication_classes = (TokenAuthentication, )
    # permission_classes = (IsAuthenticated, )




class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:
            movie = Movie.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user
            try:
                rating = Rating.objects.get(user=user.id, movie=movie.id)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                response = {'message': "Rating updated", 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating = Rating.objects.create(user=user, movie=movie, stars=stars)
                serializer = RatingSerializer(rating, many=False)
                response = {'message': "Rating created", 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)

        else:
            response = {'message': "Pass stars"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)







class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

# here i am overriding the built-in methods for update and create
    def update(self, request, *args, **kwargs):
        response = {'message': "You cant update ratings like that"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {'message': "You cant create ratings like that"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
