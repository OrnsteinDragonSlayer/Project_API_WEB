import requests


# id ключ с сайта openweathermap.org, оттуда берутся все данные
appid = 'b0aba8de435e22697c2ff6f1cf2bc6b5'


# функция возвращает словесное представление направления ветра
def get_wind_direction(deg):
    wind = ['Северный ', 'Северо-Восточный', ' Восточный',
            'Юго-Восточный', 'Южный ', 'Юго-Западный',
            ' Западный', 'Северо-Западный']
    for i in range(len(wind)):
        step = 45
        mini = i * step - 45 / 2
        maxi = i * step + 45 / 2
        if i == 0 and deg > 360 - 45 / 2:
            deg = deg - 360
        if deg >= mini and deg <= maxi:
            res = wind[i]
            break
    return res


# проверка наличия в базе информации о нужном населенном пункте
def get_city_id(city):
    try:
        res = requests.get('http://api.openweathermap.org/data/2.5/find',
                           params={'q': city, 'type': 'like', 'units': 'metric',
                                   'lang': 'ru', 'APPID': appid})
        data = res.json()
        city_id = data['list'][0]['id']
    except Exception as e:
        return f'Exception (find):, {e}'
    return city_id


# запрос текущей погоды
def request_current_weather(city_id):
    try:
        res = requests.get('http://api.openweathermap.org/data/2.5/weather',
                           params={'id': city_id, 'units': 'metric',
                                   'lang': 'ru', 'APPID': appid})
        data = res.json()
        positions_one_day = {'city': data['name'], 'country': data['sys']['country'],
                             'weather': data['weather'][0]['description'],
                             'temp': data['main']['temp'],
                             'min_temp': data['main']['temp_min'],
                             'max_temp': data['main']['temp_max'],
                             'feels_like': data['main']['feels_like'],
                             'pressure': data['main']['pressure'],
                             'visibility': data['visibility']}
        return positions_one_day
    except Exception as e:
        return f'Exception (weather):, {e}'


# прогноз на несколько дней
def request_forecast(city_id):
    try:
        res = requests.get('http://api.openweathermap.org/data/2.5/forecast',
                           params={'id': city_id, 'units': 'metric',
                                   'lang': 'ru', 'APPID': appid})
        data = res.json()
        positions_days = []
        for i in data['list']:
            positions = {'times': (i['dt_txt'])[:16],
                         'temps': '{0:+3.0f}'.format(i['main']['temp']),
                         'wind_speed': '{0:2.0f}'.format(i['wind']['speed']),
                         'wind_direction': get_wind_direction(i['wind']['deg']),
                         'weather': i['weather'][0]['description']}
            positions_days.append(positions)
        return positions_days
    except Exception as e:
        return f'Exception (forecast):, {e}'
