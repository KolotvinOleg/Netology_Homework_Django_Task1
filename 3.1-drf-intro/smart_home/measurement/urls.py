from django.urls import path
from .views import SensorsView, OneSensorView, MeasurementView

urlpatterns = [
    path('sensors/', SensorsView.as_view()),
    path('sensors/<pk>/', OneSensorView.as_view()),
    path('measurements/', MeasurementView.as_view()),
]
