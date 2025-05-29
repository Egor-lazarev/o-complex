import requests
from django.shortcuts import render
# from pprint import pprint

from weather.constants import MIN_DAYS
from weather.exceptions import CoordsApiError, CoordsKeyError
from weather.forms import WeatherForm


def decode_weather_code(code):
    weather_map = {
        0: 'Ясно ☀️',
        1: 'Преимущественно ясно 🌤',
        2: 'Переменная облачность ⛅',
        3: 'Облачно ☁️',
        45: 'Туман 🌫',
        48: 'Туман с инеем ❄️🌫',
        51: 'Слабая морось 🌧',
        53: 'Умеренная морось 🌧🌧',
        55: 'Сильная морось 🌧🌧🌧',
        56: 'Слабая ледяная морось 💦❄️',
        57: 'Сильная ледяная морось 💦💦❄️',
        61: 'Небольшой дождь 🌦',
        63: 'Умеренный дождь 🌧',
        65: 'Сильный дождь 🌧🌧',
        66: 'Ледяной дождь (слабый) 💧❄️',
        67: 'Ледяной дождь (сильный) 💧💧❄️',
        71: 'Небольшой снег ❄️',
        73: 'Умеренный снег ❄️❄️',
        75: 'Сильный снег ❄️❄️❄️',
        77: 'Снежная крупа 🌨',
        80: 'Слабый дождевой ливень 💦',
        81: 'Умеренный дождевой ливень 💦💦',
        82: 'Сильный дождевой ливень 💦💦💦',
        85: 'Слабый снежный ливень ❄️💦',
        86: 'Сильный снежный ливень ❄️❄️💦',
        95: 'Гроза ⚡',
        96: 'Гроза с мелким градом ⚡🧊',
        99: 'Гроза с крупным градом ⚡🧊🧊'
    }
    return weather_map.get(code, f'Неизвестный код погоды: {code} ❓')


def get_coords(city_name):
    geocoding_url = 'https://geocoding-api.open-meteo.com/v1/search'
    try:
        response = requests.get(
            geocoding_url, params={'name': city_name, 'count': 1}
        ).json()
    except requests.exceptions.RequestException:
        raise CoordsApiError('К сожалению возникла ошибка с внешним API')
    if not response.get('results'):
        raise CoordsKeyError('Такого города не существует.')
    latitude = response['results'][0]['latitude']
    longitude = response['results'][0]['longitude']
    return latitude, longitude


def weather_view(request):
    form = WeatherForm(request.GET or None)
    context = {'form': form}
    if form.is_valid():
        weather = None
        city = form.cleaned_data['city_name']
        days = form.cleaned_data['days'] or MIN_DAYS
        try:
            lat, long = get_coords(city)
            weather_url = 'https://api.open-meteo.com/v1/forecast'
            params = {
                'latitude': lat,
                'longitude': long,
                'current': [
                    'temperature_2m',
                    'relative_humidity_2m',
                    'apparent_temperature',
                    'pressure_msl',
                    'precipitation',
                    'rain',
                    'showers',
                    'snowfall',
                    'weather_code',
                    'cloud_cover',
                    'wind_speed_10m',
                    'wind_direction_10m'
                ],
                'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code',
                'timezone': 'auto',
                'forecast_days': days
            }
            weather = requests.get(weather_url, params=params).json()
            if 'daily' in weather:
                daily_forecast = []
                for i in range(len(weather['daily']['time'])):
                    day_data = {
                        'date': weather['daily']['time'][i],
                        'temp_max': weather['daily']['temperature_2m_max'][i],
                        'temp_min': weather['daily']['temperature_2m_min'][i],
                        'precipitation': weather['daily']['precipitation_sum'][i],
                        'weather_code': decode_weather_code(
                            weather['daily']['weather_code'][i]
                        ),
                    }
                    daily_forecast.append(day_data)
                weather['daily_forecast'] = daily_forecast
        except CoordsApiError as error:
            form.add_error(None, str(error))
        except CoordsKeyError as error:
            form.add_error('city_name', str(error))
        except requests.exceptions.RequestException:
            form.add_error(None, 'К сожалению возникла ошибка с внешним API')
        except Exception as error:
            form.add_error(None, f'Произошла ошибка: {str(error)}')
        if weather:
            context['weather'] = weather
    return render(request, 'weather/weather.html', context)
