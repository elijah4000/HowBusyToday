from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DateFactor",
            fields=[
                ("date", models.DateField(primary_key=True, serialize=False)),
                ("is_weekend", models.BooleanField(default=False)),
                ("is_stat_holiday", models.BooleanField(default=False)),
            ],
            options={"ordering": ["date"]},
        ),
        migrations.CreateModel(
            name="Park",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("slug", models.SlugField(unique=True)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("waterpark", "Waterpark"),
                            ("theme_park", "Theme Park"),
                            ("zoo", "Zoo"),
                        ],
                        max_length=20,
                    ),
                ),
                ("latitude", models.FloatField()),
                ("longitude", models.FloatField()),
                ("timezone", models.CharField(max_length=64)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="WeatherForecast",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("predicted_temp_c", models.FloatField()),
                (
                    "rain_chance_percent",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ]
                    ),
                ),
                (
                    "park",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="weather_forecasts",
                        to="parks.park",
                    ),
                ),
            ],
            options={
                "ordering": ["date"],
                "unique_together": {("park", "date")},
            },
        ),
        migrations.CreateModel(
            name="CrowdPrediction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("target_date", models.DateField()),
                (
                    "crowd_score",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(10),
                        ]
                    ),
                ),
                (
                    "confidence_score",
                    models.FloatField(
                        validators=[
                            django.core.validators.MinValueValidator(0.0),
                            django.core.validators.MaxValueValidator(1.0),
                        ]
                    ),
                ),
                (
                    "park",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="crowd_predictions",
                        to="parks.park",
                    ),
                ),
            ],
            options={
                "ordering": ["target_date"],
                "unique_together": {("park", "target_date")},
            },
        ),
    ]
