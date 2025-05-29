from django import forms

from weather.constants import MAX_DAYS, MIN_DAYS, RUS_ALPHABET


class WeatherForm(forms.Form):
    city_name = forms.CharField(
        max_length=60,
        label='Название города',
        help_text='Латиницей'
    )
    days = forms.IntegerField(
        label='Дней вперед',
        required=False,
        help_text='Необязательное поле'
    )

    def clean_city_name(self):
        city_name = self.cleaned_data.get('city_name')
        for letter in city_name:
            if letter in RUS_ALPHABET:
                raise forms.ValidationError(
                    'Необходимо ввести название города на латинице'
                )
        return city_name

    def clean_days(self):
        days = self.cleaned_data.get('days', MIN_DAYS)
        if days and (days < MIN_DAYS or days > MAX_DAYS):
            raise forms.ValidationError(
                'Можно запросить прогноз от 1 до 16 дней'
            )
        return days
