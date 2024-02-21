from django.shortcuts import render
from rest_framework.views import APIView, status, Request,Response
from movies.models import Movie
from movies.serializers import MovieSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import MyCustomPermission
from rest_framework.pagination import PageNumberPagination

class MovieView(APIView, PageNumberPagination):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (MyCustomPermission,)
    
    def get(self, request: Request):
        movies = Movie.objects.all()
        result_page = self.paginate_queryset(movies, request, view=self)
        serializer = MovieSerializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request: Request):
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status.HTTP_201_CREATED)

class MovieDetailsView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (MyCustomPermission,)
    
    def get(self, request:Request, movie_id:int):
        try:
            found_movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return Response({
                "detail": "Not found."
            }, status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(found_movie)
        return Response(serializer.data,status.HTTP_200_OK)

    def delete(self,request:Request,movie_id: int) -> Response:
        try:
            found_movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return Response({
                "detail": "Not found."
            },status.HTTP_404_NOT_FOUND)
        found_movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)