from datetime import date
from unittest.mock import MagicMock

from django.test import SimpleTestCase

from parks.models import Park
from parks.services.prediction import CrowdPredictionService


class CrowdPredictionServiceTests(SimpleTestCase):
    def setUp(self):
        self.service = CrowdPredictionService()
        self.waterpark = MagicMock(category=Park.Category.WATERPARK)
        self.theme = MagicMock(category=Park.Category.THEME_PARK)

    def test_weekend_holiday_raises_score(self):
        factor = MagicMock(is_weekend=True, is_stat_holiday=True)
        score, confidence = self.service.predict(
            self.theme, date(2026, 7, 4), date_factor=factor, weather=None
        )
        self.assertGreaterEqual(score, 8)
        self.assertEqual(confidence, 0.73)

    def test_waterpark_rain_and_cold_lowers_score(self):
        factor = MagicMock(is_weekend=False, is_stat_holiday=False)
        weather = MagicMock(predicted_temp_c=15.0, rain_chance_percent=80)
        score, _ = self.service.predict(
            self.waterpark,
            date(2026, 7, 5),
            date_factor=factor,
            weather=weather,
        )
        self.assertLessEqual(score, 2)
