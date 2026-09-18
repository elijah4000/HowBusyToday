from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Park(models.Model):
    class Category(models.TextChoices):
        WATERPARK = "waterpark", "Waterpark"
        THEME_PARK = "theme_park", "Theme Park"
        ZOO = "zoo", "Zoo"

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=Category.choices)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timezone = models.CharField(max_length=64)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class DateFactor(models.Model):
    date = models.DateField(primary_key=True)
    is_weekend = models.BooleanField(default=False)
    is_stat_holiday = models.BooleanField(default=False)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        flags = []
        if self.is_weekend:
            flags.append("weekend")
        if self.is_stat_holiday:
            flags.append("holiday")
        suffix = f" ({', '.join(flags)})" if flags else ""
        return f"{self.date}{suffix}"


class WeatherForecast(models.Model):
    park = models.ForeignKey(
        Park,
        on_delete=models.CASCADE,
        related_name="weather_forecasts",
    )
    date = models.DateField()
    predicted_temp_c = models.FloatField()
    rain_chance_percent = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        ordering = ["date"]
        unique_together = [("park", "date")]

    def __str__(self):
        return f"{self.park.slug} @ {self.date}: {self.predicted_temp_c}°C"


class CrowdPrediction(models.Model):
    park = models.ForeignKey(
        Park,
        on_delete=models.CASCADE,
        related_name="crowd_predictions",
    )
    target_date = models.DateField()
    crowd_score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    confidence_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )

    class Meta:
        ordering = ["target_date"]
        unique_together = [("park", "target_date")]

    def __str__(self):
        return f"{self.park.slug} @ {self.target_date}: {self.crowd_score}/10"
