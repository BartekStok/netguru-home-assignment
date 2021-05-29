from rest_framework import serializers
from .models import Car, Rating


class CarSerializer(serializers.ModelSerializer):
    """
    Serializer for :model: Car
    """

    rate_count = serializers.CharField(source="get_rate_count", required=False)

    class Meta:
        model = Car
        fields = ("id", "car_make", "model_name", "rate_count")
        read_only_fields = ("rate_count",)


class RatingSerializer(serializers.ModelSerializer):
    """
    Serializer for :model: Rating
    """

    class Meta:
        model = Rating
        fields = ("id", "car", "rating")
