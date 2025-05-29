from django.urls import path
from weather.views import weather_view


app_name = 'weather'


urlpatterns = [
    path('', weather_view, name='weather'),
]
