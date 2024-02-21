from django.urls import path
from movies_orders.views import MovieOrderDetailsView


urlpatterns = [
    path('movies/<int:movie_id>/orders/',MovieOrderDetailsView.as_view())
]