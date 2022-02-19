
"""when run, this script will just pront a bunch of stuff"""
import geocoder
import time
import json
import MasterConfig
from datetime import datetime
from rich.console import Console
from rich.theme import Theme
from rich.text import Text

console = Console(theme=MasterConfig.custom_theme)


def scaled_color(temp):
    """Scale the color value based on whats passed in"""
    temp = int(round(float(temp)))
    if temp > 110 or temp < 0:
        raise Exception('Temp out of bounds')
    r = g = b = 0
    if temp < 37:
        b = 255
        g = round((temp / 36) * 255)
    elif temp < 74:
        g = 255
        b = 255 - round((temp/74)*255)
    else:
        r = round((temp/110)*255)
    return "#{0:02x}{1:02x}{2:02x}".format(r, g, b)


def print_hourly_forecast(data):
    # the 0 index is the current point, which we don't want
    for i in range(1, 13, 1):
        point = data['hourly'][i]
        # get the unix timestamp
        ts = point['dt']
        # find out which hour it corresponds to
        hour = int(datetime.fromtimestamp(ts).strftime("%H"))
        # convert if > 12
        if hour > 12:
            hour = hour - 12
            sufix = 'pm'
        else:
            if hour > 11:
                sufix = 'pm'
            else:
                if hour < 1:
                    hour = hour + 12
                    sufix = 'pm'
                else:
                    sufix = 'am'
        spacing = '  '
        if hour != 10 and hour != 11 and hour != 12:
            spacing = '   '
        # print data for that point
        # color = scaled_color(point["temp"])
        # MasterConfig.colors['temp'] = color
        # console = Console(theme=Theme({"temp": color}))
        print(
            f'{hour}{sufix}{spacing}{point["temp"]:.0f}°F   {point["wind_speed"]:.0f}mph   {point["weather"][0]["description"]}')
    pass


def main():
    console = Console(theme=MasterConfig.custom_theme)
    with open('data\\weather_data.json', ) as file:
        data = json.load(file)
    with open(f'data\\forecast_data.json', ) as file:
        forecast = json.load(file)
    # print(json.dumps(data, indent=4))

    # for now, we are going to assume that jarvis will
    # do all of the 'fixing' to all values will be in desired format
    # before they are written to the json file
    # ------header------
    print(f'Weather for {data["name"]}:\n')
    # ------levels------
    color = scaled_color(data["main"]["temp"])
    MasterConfig.colors['temp'] = color
    console.print(
        f'Temperature:    [light blue]{data["main"]["temp"]}[/light blue]°F')
    print(f'Humidity:       {data["main"]["humidity"]}%')
    # still need units
    print(f'Pressure:       {data["main"]["pressure"]} hPa')
    print(f'Wind speed:     {data["wind"]["speed"]} mph {data["wind"]["deg"]}')
    if 'gust' in data['wind'].keys():
        print(f'Wind gust:      {data["wind"]["gust"]} mph\n')
    # ------current state------
    print(f'State:          {data["weather"][0]["description"].upper()}')
    print(f'Visibility:     {data["visibility"]} ft\n')
    # ------sun stuff------
    print(f'Sunrise:        {data["sys"]["sunrise"]} am')
    print(f'Sunset:         {data["sys"]["sunset"]} pm\n')
    # ------forecast------
    print(f'Hourly Forecast:')
    print_hourly_forecast(forecast)
    # sleep for a while to keep the window open
    time.sleep(100000)


if __name__ == '__main__':
    main()
