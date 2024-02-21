from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView, status, Request,Response
from movies.models import Movie
from rest_framework_simplejwt.authentication import JWTAuthentication

from movies_orders.serializers import MovieOrderSerializer

class MovieOrderDetailsView(APIView):
    authentication_classes = (JWTAuthentication,)
    
    def post(self, request:Request, movie_id:int):
        if not request.user.is_authenticated:
            return Response({"detail": "User not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            found_movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return Response({
                "detail": "Not found."
            }, status.HTTP_404_NOT_FOUND)
        serializer = MovieOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save(user=request.user, movie=found_movie)
        return Response(MovieOrderSerializer(order).data,status.HTTP_201_CREATED)
