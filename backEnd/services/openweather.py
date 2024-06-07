
import os
import requests

api_key = os.environ['api_key_previsao_tempo']

def getOpenWeather(localidade: str):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={localidade}&appid={api_key}'
    return  requests.get(url)