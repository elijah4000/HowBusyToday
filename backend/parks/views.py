from datetime import timedelta

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CrowdPrediction, DateFactor, Park, WeatherForecast
from .serializers import ParkForecastSerializer, ParkSerializer


class ParkListView(generics.ListAPIView):
    """List parks with optional category filter and name/slug search."""

    queryset = Park.objects.all()
    serializer_class = ParkSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["category"]
    search_fields = ["name", "slug"]


class ParkForecastView(APIView):
    """Park details plus the next 7 days of crowd + weather forecast."""

    def get(self, request, slug: str):
        park = get_object_or_404(Park, slug=slug)
        today = timezone.localdate()
        end = today + timedelta(days=6)
        dates = [today + timedelta(days=i) for i in range(7)]

        weather_by_date = {
            w.date: w
            for w in WeatherForecast.objects.filter(
                park=park, date__gte=today, date__lte=end
            )
        }
        crowd_by_date = {
            c.target_date: c
            for c in CrowdPrediction.objects.filter(
                park=park, target_date__gte=today, target_date__lte=end
            )
        }
        factors_by_date = {
            d.date: d
            for d in DateFactor.objects.filter(date__gte=today, date__lte=end)
        }

        forecast = []
        for day in dates:
            weather = weather_by_date.get(day)
            crowd = crowd_by_date.get(day)
            factor = factors_by_date.get(day)
            forecast.append(
                {
                    "date": day,
                    "crowd_score": crowd.crowd_score if crowd else None,
                    "confidence_score": crowd.confidence_score if crowd else None,
                    "predicted_temp_c": (
                        weather.predicted_temp_c if weather else None
                    ),
                    "rain_chance_percent": (
                        weather.rain_chance_percent if weather else None
                    ),
                    "is_weekend": factor.is_weekend if factor else day.weekday() >= 5,
                    "is_stat_holiday": factor.is_stat_holiday if factor else False,
                }
            )

        payload = {"park": park, "forecast": forecast}
        return Response(ParkForecastSerializer(payload).data)
