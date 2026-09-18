from django.urls import path

from .views import ParkForecastView, ParkListView

urlpatterns = [
    path("parks/", ParkListView.as_view(), name="park-list"),
    path(
        "parks/<slug:slug>/forecast/",
        ParkForecastView.as_view(),
        name="park-forecast",
    ),
]
