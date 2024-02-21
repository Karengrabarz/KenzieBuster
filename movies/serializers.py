from rest_framework import serializers
from movies.models import Movie, RatingOptions

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10, allow_blank=True, default="")
    rating = serializers.ChoiceField(
        choices=RatingOptions.choices,
        default=RatingOptions.G
    )
    synopsis = serializers.CharField(
        allow_blank=True,
        default= ''
    )
    added_by = serializers.SerializerMethodField()
    def get_added_by(self, movie):
        return movie.user.email

    # added_by = serializers.CharField(source='movie.user.email', read_only=True)
  
    def create(self, validated_data):
        return Movie.objects.create(**validated_data)

   

