from datetime import timedelta
import hashlib

from django.core.management.base import BaseCommand
from django.utils import timezone

from parks.models import CrowdPrediction, DateFactor, Park, WeatherForecast
from parks.services.prediction import CrowdPredictionService


# Existing regional demo parks (fictional) + Six Flags portfolio parks.
SAMPLE_PARKS = [
    # --- Regional demo parks ---
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
    {
        "name": "Okanagan Rapids Waterpark",
        "slug": "okanagan-rapids",
        "category": Park.Category.WATERPARK,
        "latitude": 49.8880,
        "longitude": -119.4960,
        "timezone": "America/Vancouver",
    },
    {
        "name": "Harbourfront Adventure Park",
        "slug": "harbourfront-adventure",
        "category": Park.Category.THEME_PARK,
        "latitude": 43.6400,
        "longitude": -79.3800,
        "timezone": "America/Toronto",
    },
    {
        "name": "Great Lakes Wildlife Zoo",
        "slug": "great-lakes-zoo",
        "category": Park.Category.ZOO,
        "latitude": 43.6532,
        "longitude": -79.3832,
        "timezone": "America/Toronto",
    },
    {
        "name": "Atlantic Tide Waterpark",
        "slug": "atlantic-tide",
        "category": Park.Category.WATERPARK,
        "latitude": 44.6488,
        "longitude": -63.5752,
        "timezone": "America/Halifax",
    },
    {
        "name": "Maple Ridge Theme Park",
        "slug": "maple-ridge",
        "category": Park.Category.THEME_PARK,
        "latitude": 45.5017,
        "longitude": -73.5673,
        "timezone": "America/Toronto",
    },
    {
        "name": "Assiniboine Wildlife Park",
        "slug": "assiniboine-wildlife",
        "category": Park.Category.ZOO,
        "latitude": 49.8844,
        "longitude": -97.1470,
        "timezone": "America/Winnipeg",
    },
    {
        "name": "Sunshine Coast Splash Zone",
        "slug": "sunshine-coast-splash",
        "category": Park.Category.WATERPARK,
        "latitude": 49.3990,
        "longitude": -123.5080,
        "timezone": "America/Vancouver",
    },
    {
        "name": "Foothills Funland",
        "slug": "foothills-funland",
        "category": Park.Category.THEME_PARK,
        "latitude": 51.0500,
        "longitude": -114.2500,
        "timezone": "America/Edmonton",
    },
    {
        "name": "Capital Region Zoo",
        "slug": "capital-region-zoo",
        "category": Park.Category.ZOO,
        "latitude": 45.4215,
        "longitude": -75.6972,
        "timezone": "America/Toronto",
    },
    {
        "name": "Kawartha Lakes Waterpark",
        "slug": "kawartha-lakes",
        "category": Park.Category.WATERPARK,
        "latitude": 44.3500,
        "longitude": -78.7500,
        "timezone": "America/Toronto",
    },
    {
        "name": "Island Coaster Park",
        "slug": "island-coaster",
        "category": Park.Category.THEME_PARK,
        "latitude": 48.4284,
        "longitude": -123.3656,
        "timezone": "America/Vancouver",
    },
    {
        "name": "Prairie Sky Zoo",
        "slug": "prairie-sky-zoo",
        "category": Park.Category.ZOO,
        "latitude": 52.1579,
        "longitude": -106.6702,
        "timezone": "America/Regina",
    },
    # --- Six Flags theme / amusement parks ---
    {
        "name": "California's Great America",
        "slug": "californias-great-america",
        "category": Park.Category.THEME_PARK,
        "latitude": 37.3970,
        "longitude": -121.9740,
        "timezone": "America/Los_Angeles",
    },
    {
        "name": "Knott's Berry Farm",
        "slug": "knotts-berry-farm",
        "category": Park.Category.THEME_PARK,
        "latitude": 33.8440,
        "longitude": -118.0000,
        "timezone": "America/Los_Angeles",
    },
    {
        "name": "Six Flags Magic Mountain",
        "slug": "six-flags-magic-mountain",
        "category": Park.Category.THEME_PARK,
        "latitude": 34.4250,
        "longitude": -118.5970,
        "timezone": "America/Los_Angeles",
    },
    {
        "name": "Six Flags Discovery Kingdom",
        "slug": "six-flags-discovery-kingdom",
        "category": Park.Category.THEME_PARK,
        "latitude": 38.1380,
        "longitude": -122.2330,
        "timezone": "America/Los_Angeles",
    },
    {
        "name": "Six Flags Over Georgia",
        "slug": "six-flags-over-georgia",
        "category": Park.Category.THEME_PARK,
        "latitude": 33.7700,
        "longitude": -84.5510,
        "timezone": "America/New_York",
    },
    {
        "name": "Six Flags Great America",
        "slug": "six-flags-great-america",
        "category": Park.Category.THEME_PARK,
        "latitude": 42.3660,
        "longitude": -87.9340,
        "timezone": "America/Chicago",
    },
    {
        "name": "Six Flags New England",
        "slug": "six-flags-new-england",
        "category": Park.Category.THEME_PARK,
        "latitude": 42.0380,
        "longitude": -72.6150,
        "timezone": "America/New_York",
    },
    {
        "name": "Six Flags Great Adventure",
        "slug": "six-flags-great-adventure",
        "category": Park.Category.THEME_PARK,
        "latitude": 40.1380,
        "longitude": -74.4410,
        "timezone": "America/New_York",
    },
    {
        "name": "Wild Safari Adventure",
        "slug": "wild-safari-adventure",
        "category": Park.Category.ZOO,
        "latitude": 40.1360,
        "longitude": -74.4400,
        "timezone": "America/New_York",
    },
    {
        "name": "Six Flags Darien Lake",
        "slug": "six-flags-darien-lake",
        "category": Park.Category.THEME_PARK,
        "latitude": 42.9290,
        "longitude": -78.3850,
        "timezone": "America/New_York",
    },
    {
        "name": "Carowinds",
        "slug": "carowinds",
        "category": Park.Category.THEME_PARK,
        "latitude": 35.1040,
        "longitude": -80.9390,
        "timezone": "America/New_York",
    },
    {
        "name": "Cedar Point",
        "slug": "cedar-point",
        "category": Park.Category.THEME_PARK,
        "latitude": 41.4820,
        "longitude": -82.6830,
        "timezone": "America/New_York",
    },
    {
        "name": "Kings Island",
        "slug": "kings-island",
        "category": Park.Category.THEME_PARK,
        "latitude": 39.3450,
        "longitude": -84.2660,
        "timezone": "America/New_York",
    },
    {
        "name": "Frontier City",
        "slug": "frontier-city",
        "category": Park.Category.THEME_PARK,
        "latitude": 35.5850,
        "longitude": -97.4440,
        "timezone": "America/Chicago",
    },
    {
        "name": "Dorney Park",
        "slug": "dorney-park",
        "category": Park.Category.THEME_PARK,
        "latitude": 40.5790,
        "longitude": -75.5350,
        "timezone": "America/New_York",
    },
    {
        "name": "Six Flags Over Texas",
        "slug": "six-flags-over-texas",
        "category": Park.Category.THEME_PARK,
        "latitude": 32.7550,
        "longitude": -97.0700,
        "timezone": "America/Chicago",
    },
    {
        "name": "Six Flags Fiesta Texas",
        "slug": "six-flags-fiesta-texas",
        "category": Park.Category.THEME_PARK,
        "latitude": 29.5990,
        "longitude": -98.6090,
        "timezone": "America/Chicago",
    },
    {
        "name": "Kings Dominion",
        "slug": "kings-dominion",
        "category": Park.Category.THEME_PARK,
        "latitude": 37.8400,
        "longitude": -77.4440,
        "timezone": "America/New_York",
    },
    {
        "name": "Canada's Wonderland",
        "slug": "canadas-wonderland",
        "category": Park.Category.THEME_PARK,
        "latitude": 43.8430,
        "longitude": -79.5420,
        "timezone": "America/Toronto",
    },
    {
        "name": "La Ronde",
        "slug": "la-ronde",
        "category": Park.Category.THEME_PARK,
        "latitude": 45.5220,
        "longitude": -73.5350,
        "timezone": "America/Toronto",
    },
    {
        "name": "Six Flags México",
        "slug": "six-flags-mexico",
        "category": Park.Category.THEME_PARK,
        "latitude": 19.2950,
        "longitude": -99.2090,
        "timezone": "America/Mexico_City",
    },
    {
        "name": "Six Flags St. Louis",
        "slug": "six-flags-st-louis",
        "category": Park.Category.THEME_PARK,
        "latitude": 38.5130,
        "longitude": -90.6750,
        "timezone": "America/Chicago",
    },
    {
        "name": "Six Flags Great Escape",
        "slug": "six-flags-great-escape",
        "category": Park.Category.THEME_PARK,
        "latitude": 43.3510,
        "longitude": -73.6900,
        "timezone": "America/New_York",
    },
    {
        "name": "Valleyfair",
        "slug": "valleyfair",
        "category": Park.Category.THEME_PARK,
        "latitude": 44.7990,
        "longitude": -93.4570,
        "timezone": "America/Chicago",
    },
    {
        "name": "Worlds of Fun",
        "slug": "worlds-of-fun",
        "category": Park.Category.THEME_PARK,
        "latitude": 39.1730,
        "longitude": -94.4880,
        "timezone": "America/Chicago",
    },
    {
        "name": "Michigan's Adventure",
        "slug": "michigans-adventure",
        "category": Park.Category.THEME_PARK,
        "latitude": 43.3430,
        "longitude": -86.2770,
        "timezone": "America/Detroit",
    },
    # --- Six Flags waterparks ---
    {
        "name": "Six Flags Hurricane Harbor Phoenix",
        "slug": "hurricane-harbor-phoenix",
        "category": Park.Category.WATERPARK,
        "latitude": 33.5320,
        "longitude": -112.2610,
        "timezone": "America/Phoenix",
    },
    {
        "name": "Knott's Soak City",
        "slug": "knotts-soak-city",
        "category": Park.Category.WATERPARK,
        "latitude": 33.8410,
        "longitude": -117.9980,
        "timezone": "America/Los_Angeles",
    },
    {
        "name": "Six Flags Hurricane Harbor Los Angeles",
        "slug": "hurricane-harbor-los-angeles",
        "category": Park.Category.WATERPARK,
        "latitude": 34.4240,
        "longitude": -118.5950,
        "timezone": "America/Los_Angeles",
    },
    {
        "name": "Six Flags Hurricane Harbor Concord",
        "slug": "hurricane-harbor-concord",
        "category": Park.Category.WATERPARK,
        "latitude": 37.9740,
        "longitude": -122.0330,
        "timezone": "America/Los_Angeles",
    },
    {
        "name": "Six Flags White Water",
        "slug": "six-flags-white-water",
        "category": Park.Category.WATERPARK,
        "latitude": 33.9590,
        "longitude": -84.5300,
        "timezone": "America/New_York",
    },
    {
        "name": "Six Flags Hurricane Harbor Chicago",
        "slug": "hurricane-harbor-chicago",
        "category": Park.Category.WATERPARK,
        "latitude": 42.3680,
        "longitude": -87.9360,
        "timezone": "America/Chicago",
    },
    {
        "name": "Six Flags Hurricane Harbor Rockford",
        "slug": "hurricane-harbor-rockford",
        "category": Park.Category.WATERPARK,
        "latitude": 42.2350,
        "longitude": -88.9700,
        "timezone": "America/Chicago",
    },
    {
        "name": "Six Flags Hurricane Harbor New Jersey",
        "slug": "hurricane-harbor-new-jersey",
        "category": Park.Category.WATERPARK,
        "latitude": 40.1400,
        "longitude": -74.4430,
        "timezone": "America/New_York",
    },
    {
        "name": "Cedar Point Shores",
        "slug": "cedar-point-shores",
        "category": Park.Category.WATERPARK,
        "latitude": 41.4840,
        "longitude": -82.6850,
        "timezone": "America/New_York",
    },
    {
        "name": "Six Flags Hurricane Harbor Oklahoma City",
        "slug": "hurricane-harbor-oklahoma-city",
        "category": Park.Category.WATERPARK,
        "latitude": 35.5240,
        "longitude": -97.4760,
        "timezone": "America/Chicago",
    },
    {
        "name": "Six Flags Hurricane Harbor Arlington",
        "slug": "hurricane-harbor-arlington",
        "category": Park.Category.WATERPARK,
        "latitude": 32.7570,
        "longitude": -97.0680,
        "timezone": "America/Chicago",
    },
    {
        "name": "Six Flags Hurricane Harbor Splashtown",
        "slug": "hurricane-harbor-splashtown",
        "category": Park.Category.WATERPARK,
        "latitude": 30.0540,
        "longitude": -95.4290,
        "timezone": "America/Chicago",
    },
    {
        "name": "Schlitterbahn Waterpark New Braunfels",
        "slug": "schlitterbahn-new-braunfels",
        "category": Park.Category.WATERPARK,
        "latitude": 29.7060,
        "longitude": -98.1200,
        "timezone": "America/Chicago",
    },
    {
        "name": "Schlitterbahn Waterpark Galveston",
        "slug": "schlitterbahn-galveston",
        "category": Park.Category.WATERPARK,
        "latitude": 29.2700,
        "longitude": -94.8400,
        "timezone": "America/Chicago",
    },
    {
        "name": "Six Flags Hurricane Harbor Oaxtepec",
        "slug": "hurricane-harbor-oaxtepec",
        "category": Park.Category.WATERPARK,
        "latitude": 18.9060,
        "longitude": -98.9700,
        "timezone": "America/Mexico_City",
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
