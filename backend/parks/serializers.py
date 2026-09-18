from rest_framework import serializers

from .models import CrowdPrediction, DateFactor, Park, WeatherForecast


class ParkSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(
        source="get_category_display", read_only=True
    )

    class Meta:
        model = Park
        fields = [
            "id",
            "name",
            "slug",
            "category",
            "category_display",
            "latitude",
            "longitude",
            "timezone",
        ]


class WeatherForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherForecast
        fields = ["date", "predicted_temp_c", "rain_chance_percent"]


class CrowdPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrowdPrediction
        fields = ["target_date", "crowd_score", "confidence_score"]


class DateFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateFactor
        fields = ["date", "is_weekend", "is_stat_holiday"]


class DayForecastSerializer(serializers.Serializer):
    date = serializers.DateField()
    crowd_score = serializers.IntegerField(allow_null=True)
    confidence_score = serializers.FloatField(allow_null=True)
    predicted_temp_c = serializers.FloatField(allow_null=True)
    rain_chance_percent = serializers.IntegerField(allow_null=True)
    is_weekend = serializers.BooleanField(default=False)
    is_stat_holiday = serializers.BooleanField(default=False)


class ParkForecastSerializer(serializers.Serializer):
    park = ParkSerializer()
    forecast = DayForecastSerializer(many=True)
