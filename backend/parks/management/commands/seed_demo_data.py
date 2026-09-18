from datetime import timedelta
import hashlib

from django.core.management.base import BaseCommand
from django.utils import timezone

from parks.models import CrowdPrediction, DateFactor, Park, WeatherForecast
from parks.services.prediction import CrowdPredictionService


SAMPLE_PARKS = [
    {
        "name": "Wild Waves Waterpark",
        "slug": "wild-waves",
        "category": Park.Category.WATERPARK,
        "latitude": 49.0504,
        "longitude": -122.3045,
        "timezone": "America/Vancouver",
    },
    {
        "name": "Pacific Coaster Theme Park",
        "slug": "pacific-coaster",
        "category": Park.Category.THEME_PARK,
        "latitude": 49.2827,
        "longitude": -123.1207,
        "timezone": "America/Vancouver",
    },
    {
        "name": "Cascade Mountain Zoo",
        "slug": "cascade-zoo",
        "category": Park.Category.ZOO,
        "latitude": 51.0447,
        "longitude": -114.0719,
        "timezone": "America/Edmonton",
    },
    {
        "name": "Prairie Splash Waterpark",
        "slug": "prairie-splash",
        "category": Park.Category.WATERPARK,
        "latitude": 52.1332,
        "longitude": -106.6700,
        "timezone": "America/Regina",
    },
    {
        "name": "Northern Lights Theme Park",
        "slug": "northern-lights",
        "category": Park.Category.THEME_PARK,
        "latitude": 53.5461,
        "longitude": -113.4938,
        "timezone": "America/Edmonton",
    },
    {
        "name": "River Valley Zoo",
        "slug": "river-valley-zoo",
        "category": Park.Category.ZOO,
        "latitude": 53.5232,
        "longitude": -113.5263,
        "timezone": "America/Edmonton",
    },
]


def _seed_float(key: str, lo: float, hi: float) -> float:
    digest = hashlib.md5(key.encode()).hexdigest()
    unit = int(digest[:8], 16) / 0xFFFFFFFF
    return lo + (hi - lo) * unit


class Command(BaseCommand):
    help = "Seed sample parks, date factors, weather, and crowd predictions."

    def handle(self, *args, **options):
        today = timezone.localdate()
        service = CrowdPredictionService()

        for park_data in SAMPLE_PARKS:
            Park.objects.update_or_create(
                slug=park_data["slug"], defaults=park_data
            )

        parks = list(Park.objects.all())

        for offset in range(14):
            day = today + timedelta(days=offset)
            DateFactor.objects.update_or_create(
                date=day,
                defaults={
                    "is_weekend": day.weekday() >= 5,
                    # Deterministic "holiday" every ~11 days for demo badges
                    "is_stat_holiday": offset in {2, 9},
                },
            )

        for park in parks:
            for offset in range(14):
                day = today + timedelta(days=offset)
                key = f"{park.slug}:{day.isoformat()}"
                temp = round(_seed_float(f"temp:{key}", 12.0, 32.0), 1)
                rain = int(_seed_float(f"rain:{key}", 5.0, 80.0))

                weather, _ = WeatherForecast.objects.update_or_create(
                    park=park,
                    date=day,
                    defaults={
                        "predicted_temp_c": temp,
                        "rain_chance_percent": rain,
                    },
                )
                factor = DateFactor.objects.get(date=day)
                crowd_score, confidence = service.predict(
                    park, day, date_factor=factor, weather=weather
                )
                CrowdPrediction.objects.update_or_create(
                    park=park,
                    target_date=day,
                    defaults={
                        "crowd_score": crowd_score,
                        "confidence_score": confidence,
                    },
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {len(parks)} parks with 14 days of forecasts."
            )
        )
