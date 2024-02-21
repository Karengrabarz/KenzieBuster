from rest_framework import serializers
from movies.models import Movie

from movies.serializers import MovieSerializer
from movies_orders.models import MovieOrder


class MovieOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    purchased_at = serializers.DateTimeField(read_only=True)
    price = serializers.DecimalField(decimal_places=2,max_digits=8)
    title = serializers.CharField(read_only=True,source='movie.title')
    purchased_by = serializers.CharField(read_only=True, source='user.email')

    def create(self, validated_data):
        return MovieOrder.objects.create(**validated_data)