"""
URL configuration for trip_planner app
"""
from django.urls import path
from . import views

urlpatterns = [
    path('calculate-trip/', views.calculate_trip, name='calculate_trip'),
    path('geocode/', views.geocode, name='geocode'),
    path('health/', views.health_check, name='health_check'),
]
