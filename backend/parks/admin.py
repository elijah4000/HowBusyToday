from django.contrib import admin

from .models import CrowdPrediction, DateFactor, Park, WeatherForecast


@admin.register(Park)
class ParkAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "category", "timezone")
    list_filter = ("category",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")


@admin.register(DateFactor)
class DateFactorAdmin(admin.ModelAdmin):
    list_display = ("date", "is_weekend", "is_stat_holiday")
    list_filter = ("is_weekend", "is_stat_holiday")


@admin.register(WeatherForecast)
class WeatherForecastAdmin(admin.ModelAdmin):
    list_display = ("park", "date", "predicted_temp_c", "rain_chance_percent")
    list_filter = ("park__category", "date")
    search_fields = ("park__name",)


@admin.register(CrowdPrediction)
class CrowdPredictionAdmin(admin.ModelAdmin):
    list_display = ("park", "target_date", "crowd_score", "confidence_score")
    list_filter = ("park__category", "target_date")
    search_fields = ("park__name",)
