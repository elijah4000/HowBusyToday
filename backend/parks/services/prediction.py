"""Heuristic crowd-score prediction for regional parks."""

from __future__ import annotations

from datetime import date

from parks.models import DateFactor, Park, WeatherForecast


class CrowdPredictionService:
    """Deterministic crowd score (1–10) from calendar + weather heuristics."""

    BASE_SCORE = 4.0

    def predict(
        self,
        park: Park,
        target_date: date,
        *,
        date_factor: DateFactor | None = None,
        weather: WeatherForecast | None = None,
    ) -> tuple[int, float]:
        """
        Return (crowd_score, confidence_score).

        crowd_score is clamped to 1–10. confidence_score is 0–1 based on
        how many input signals were available.
        """
        if date_factor is None:
            date_factor = DateFactor.objects.filter(date=target_date).first()

        if weather is None:
            weather = WeatherForecast.objects.filter(
                park=park, date=target_date
            ).first()

        score = self.BASE_SCORE
        signals = 0

        if date_factor is not None:
            signals += 1
            if date_factor.is_weekend:
                score += 2.5
            if date_factor.is_stat_holiday:
                score += 2.0

        if weather is not None:
            signals += 1
            score += self._weather_adjustment(park.category, weather)

        crowd_score = int(round(max(1.0, min(10.0, score))))
        confidence = 0.45 + (0.275 * signals)
        return crowd_score, round(confidence, 2)

    def _weather_adjustment(
        self, category: str, weather: WeatherForecast
    ) -> float:
        temp = weather.predicted_temp_c
        rain = weather.rain_chance_percent

        if category == Park.Category.WATERPARK:
            adjustment = 0.0
            # Ideal swim weather boosts attendance; cold/rain kills it.
            if temp >= 28:
                adjustment += 2.0
            elif temp >= 24:
                adjustment += 1.0
            elif temp < 18:
                adjustment -= 3.0
            elif temp < 22:
                adjustment -= 1.5

            if rain >= 60:
                adjustment -= 3.5
            elif rain >= 40:
                adjustment -= 2.0
            elif rain >= 20:
                adjustment -= 0.5
            return adjustment

        if category == Park.Category.THEME_PARK:
            adjustment = 0.0
            if temp >= 18 and temp <= 28:
                adjustment += 1.0
            elif temp < 10 or temp > 34:
                adjustment -= 1.5

            if rain >= 70:
                adjustment -= 2.0
            elif rain >= 40:
                adjustment -= 1.0
            return adjustment

        # Zoos: mild weather preferred; extreme heat or heavy rain softens crowds.
        adjustment = 0.0
        if 12 <= temp <= 26:
            adjustment += 0.5
        elif temp > 32 or temp < 5:
            adjustment -= 1.5

        if rain >= 60:
            adjustment -= 1.5
        elif rain >= 35:
            adjustment -= 0.75
        return adjustment


def predict_crowd_score(
    park: Park,
    target_date: date,
    *,
    date_factor: DateFactor | None = None,
    weather: WeatherForecast | None = None,
) -> tuple[int, float]:
    """Module-level convenience wrapper around CrowdPredictionService."""
    return CrowdPredictionService().predict(
        park,
        target_date,
        date_factor=date_factor,
        weather=weather,
    )
