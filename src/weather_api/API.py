import json
import requests
import geocoder
try:
    import MasterConfig
except ImportError:
    pass
from datetime import datetime
try:
    from weather_api.Config import *
except ImportError:
    import Config


def get_weather():
    g = geocoder.ip('me').latlng
    data = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?lat={g[0]}&lon={g[1]}&appid={API_KEY}&units=imperial').json()
    # give the current city to MasterConfig
    MasterConfig.current_city = data['name']
    # sunrise/sunset UNIX to time00:00
    sunrise_hour = int(datetime.utcfromtimestamp(
        data['sys']['sunrise']).strftime("%H")) - 4
    sunrise_min = datetime.utcfromtimestamp(
        data['sys']['sunrise']).strftime("%M")
    data['sys']['sunrise'] = f'{sunrise_hour}:{sunrise_min}'
    # sunset
    sunset_hour = int(datetime.utcfromtimestamp(
        data['sys']['sunset']).strftime("%H")) - 4
    if sunset_hour > 12:
        # convert to non-military time
        hour = sunset_hour - 12
        sunset_minute = datetime.utcfromtimestamp(
            data['sys']['sunset']).strftime("%M")
        sunset = f'{hour}:{sunset_minute}'
    else:
        sunset = datetime.utcfromtimestamp(
            data['sys']['sunset']).strftime("%H:%M")
    data['sys']['sunset'] = sunset
    # wind deg to NSEW
    deg = int(data['wind']['deg'])
    if deg > 330 and deg < 30:
        # >330 and <30 is N
        data['wind']['deg'] = 'N'
        data['wind']['direction'] = 'North'
    elif deg >= 30 and deg <= 60:
        # >=30 and <=60 is NE
        data['wind']['deg'] = 'NE'
        data['wind']['direction'] = 'Northeast'
    elif deg > 60 and deg < 120:
        # >60 and <120 is E
        data['wind']['deg'] = 'E'
        data['wind']['direction'] = 'East'
    elif deg >= 120 and deg <= 150:
        # >=120 and <=150 is SE
        data['wind']['deg'] = 'SE'
        data['wind']['direction'] = 'Southeast'
    elif deg > 150 and deg < 210:
        # >150 and <210 is S
        data['wind']['deg'] = 'S'
        data['wind']['direction'] = 'South'
    elif deg >= 210 and deg <= 240:
        # >=210 and <=240 is SW
        data['wind']['deg'] = 'SW'
        data['wind']['direction'] = 'Southwest'
    elif deg > 240 and deg < 300:
        # >240 and <300 is W
        data['wind']['deg'] = 'W'
        data['wind']['direction'] = 'West'
    else:
        # >=300 and <=330 is NW
        data['wind']['deg'] = 'NW'
        data['wind']['direction'] = 'Northwest'
    return data


def get_weather_city():
    city = 'Atlanta'
    data = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=imperial').json()
    return data


def get_hourly_forecast():
    g = geocoder.ip('me').latlng
    data = requests.get(
        f'https://api.openweathermap.org/data/2.5/onecall?lat={g[0]}&lon={g[1]}&exclude=current,minutely,alerts&appid={API_KEY}&units=imperial').json()
    for point in range(len(data['hourly'])):
        deg = int(data['hourly'][point]['wind_deg'])
    if deg > 330 and deg < 30:
        # >330 and <30 is N
        data['hourly'][point]['deg'] = 'N'
        data['hourly'][point]['direction'] = 'North'
    elif deg >= 30 and deg <= 60:
        # >=30 and <=60 is NE
        data['hourly'][point]['deg'] = 'NE'
        data['hourly'][point]['direction'] = 'Northeast'
    elif deg > 60 and deg < 120:
        # >60 and <120 is E
        data['hourly'][point]['deg'] = 'E'
        data['hourly'][point]['direction'] = 'East'
    elif deg >= 120 and deg <= 150:
        # >=120 and <=150 is SE
        data['hourly'][point]['deg'] = 'SE'
        data['hourly'][point]['direction'] = 'Southeast'
    elif deg > 150 and deg < 210:
        # >150 and <210 is S
        data['hourly'][point]['deg'] = 'S'
        data['hourly'][point]['direction'] = 'South'
    elif deg >= 210 and deg <= 240:
        # >=210 and <=240 is SW
        data['hourly'][point]['deg'] = 'SW'
        data['hourly'][point]['direction'] = 'Southwest'
    elif deg > 240 and deg < 300:
        # >240 and <300 is W
        data['hourly'][point]['deg'] = 'W'
        data['hourly'][point]['direction'] = 'West'
    else:
        # >=300 and <=330 is NW
        data['hourly'][point]['deg'] = 'NW'
        data['hourly'][point]['direction'] = 'Northwest'
    return data


if __name__ == '__main__':
    # print(json.dumps(get_weather(), indent=4, sort_keys=True))
    data = get_hourly_forecast()
    print(str(len(data['hourly'])))
    with open('example_hourly_forecast.json', 'w+') as file:
        json.dump(get_hourly_forecast(), file, indent=4)
