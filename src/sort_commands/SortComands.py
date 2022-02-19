import os
import re
import sys
import time
import json
import signal
import threading
from datetime import datetime
import webbrowser as wb
import MasterConfig
import subprocess
import paramiko
from weather_api.API import *
from news_api.API import *
from jarvis.jarvis_coms import *
from encryption_api.api import *
from tqdm import tqdm


def sort_verbal_command(command):
    """Takes verbal command as a string and determines request."""
    # launches the chrome app instead of edge(default browser)
    browser = wb.get(
        'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s')

    # ------conversation checks-------
    if bool(re.search('hello|hi|hey', command)):
        speak('Hello sir.')
    elif bool(re.search('are you there|you there', command)):
        speak('I am indeed present, waiting for your command.')
    elif bool(re.search('jarvis you up|you up', command)):
        speak('For you sir, always.')
    elif bool(re.search('thanks|thank', command)):
        speak("You're welcome sir.")
    elif bool(re.search('say hello', command)):
        speak('Hello sir.')
    elif bool(re.search('say goodbye', command)):
        speak('Goodbye sir.')
    elif bool(re.search('love you', command)):
        speak('I love you more, sir')
    elif bool(re.search('deafen|go deaf|go duff|go death|stop listening', command)):
        speak('Going deaf, say listen if you need anything sir.')
        while True:
            ans = listen()
            if bool(re.search('listen', ans)):
                break
        speak("I'm listening now sir.")

    # ------system commands------
    elif bool(re.search('note', command)):
        write_note()
        MasterConfig.process_list['notes_process'] = launch_notes_peripheral()
    elif bool(re.search('sleep', command)):
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    elif bool(re.search('shutdown|shut down', command)):
        os.system("shutdown /s /t 1")
    elif bool(re.search('close grah|close chart|close graphs|close charts', command)):
        speak('Closing charts')
        os.system("taskkill /im msedge.exe /f")
        os.system("taskkill /im chrome.exe /f")
    elif bool(re.search('launch cmd|start cmd|open cmd', command)):
        # careful with this one it may end the program
        speak('Opening terminal.')
        subprocess.Popen(['C:\\WINDOWS\\system32\\cmd.exe'])
    # ------web browsing------

    # ------command checks------
    elif bool(re.search('news', command)):
        read_out_market_news()
        read_out_crypto_news()
    elif bool(re.search('weather|whether|forecast|four cast', command)):
        get_weather_data()
        MasterConfig.process_list['weather_process'] = launch_weather_peripheral(
        )
        read_out_weather()
    elif bool(re.search('radar', command)):
        show_radar(browser)
    elif bool(re.search('start my day', command)):
        start_my_day_logic(browser)
    elif bool(re.search('refresh|update', command)):
        speak('Refreshing data.')
        return False
    elif bool(re.search('decrypt|unlock', command)):
        speak('Checking encryption status of your private folder')
        private_dir = f'{MasterConfig.cwd}\\private_data'
        if check_encryption(private_dir):
            speak('private folder currently encrypted')
            speak('please enter your password')
            if input('Password: ') == keys.PRIVATE_FOLDER_KEY:
                speak('Password correct')
                speak('decrypting your personal data...')
                decrypt_private_folder()
                speak('Welcome sir, your personal data is now accessible')
            else:
                speak('Sorry, I do not recognize you')
        else:
            speak('your private folder currently decrypted')
    elif bool(re.search('encrypt|lock', command)):
        speak('Checking encryption status of your private folder')
        private_dir = f'{MasterConfig.cwd}\\private_data'
        if check_encryption(private_dir):
            speak('private folder currently encrypted')
        else:
            speak('private folder currently decrypted')
            speak('encrypting your private folder...')
            encrypt_private_folder()
            speak('private folder now encrypted')
    elif bool(re.search('market analysis|analyze market', command)):
        get_stock_news()
        MasterConfig.process_list['news_process'] = launch_stock_news_peripheral(
        )
        read_out_market_analysis()
        read_out_market_news()
        # Crypto News
        get_crypto_news()
        MasterConfig.process_list['crypto_news_process'] = launch_crypto_news_peripheral(
        )
        read_out_crypto_analysis()
        read_out_crypto_news()
    # ------end and edge cases------
    elif bool(re.search('end processes|close windows|close all windows|close terminals|close all terminals', command)):
        speak('Closing terminals')
        end_processes()
    elif command == 'end' or command == 'jarvis end' or 'terminate' in command:
        speak('Goodbye sir.')
        sys.exit()
    else:
        # unrecognized commands that are not 'exception' just do nothing and keep listening
        pass


def read_out_market_analysis():
    """Reads out current market stats"""
    pos = MasterConfig.stock_news_analysis[0]
    neu = MasterConfig.stock_news_analysis[1]
    neg = MasterConfig.stock_news_analysis[2]
    if pos > neg:
        speak('News analysis suggests a positive market outlook.', 150)
    else:
        speak('News analysis suggests negative market outlook', 150)


def read_out_crypto_analysis():
    """Reads out current market stats"""
    pos = MasterConfig.crypto_news_analysis[0]
    neu = MasterConfig.crypto_news_analysis[1]
    neg = MasterConfig.crypto_news_analysis[2]
    if pos > neg:
        speak('Crypto news analysis suggests a positive market outlook.', 150)
    else:
        speak('Crypto news analysis suggests negative market outlook', 150)


def read_out_market_news():
    """Read out the top 3 stock headlines"""
    speak("Here's the top 3 headlines")
    for line in MasterConfig.top_3_stock_headlines:
        speak(line, 150)


def read_out_crypto_news():
    """Read out the top 3 crypto headlines"""
    speak("Here's the top 3 headlines relating to crypto")
    for line in MasterConfig.top_3_crypto_headlines:
        speak(line, 150)


def start_my_day_logic(browser):
    """Logic for the 'start my day' command"""
    # Weather
    get_weather_data()
    MasterConfig.process_list['weather_process'] = launch_weather_peripheral()
    read_out_weather()

    # Stock market news
    get_stock_news()
    MasterConfig.process_list['news_process'] = launch_stock_news_peripheral()
    read_out_market_analysis()
    read_out_market_news()
    # Crypto News
    get_crypto_news()
    MasterConfig.process_list['crypto_news_process'] = launch_crypto_news_peripheral(
    )
    read_out_crypto_analysis()
    read_out_crypto_news()
    # Finally
    speak("If you need anything, I'll be listening.")


def get_weather_data():
    """Get current weather data"""
    MasterConfig.weather_data = get_weather()
    MasterConfig.forecast = get_hourly_forecast()
    # write the data to the file so periph can access the data
    with open('data\\weather_data.json', 'w+') as file:
        json.dump(MasterConfig.weather_data, file, indent=4)

    with open('data\\forecast_data.json', 'w+') as file:
        json.dump(MasterConfig.forecast, file, indent=4)


def read_out_weather():
    """Read out the current weather"""
    text = f'The current temperature in {MasterConfig.weather_data["name"]} is {MasterConfig.weather_data["main"]["temp"]:.0f} degrees.'
    speak(text, 150)
    text = f'It is {MasterConfig.weather_data["weather"][0]["description"]} with wind speeds of {MasterConfig.weather_data["wind"]["speed"]} miles per hour from the {MasterConfig.weather_data["wind"]["direction"]}'
    speak(text, 150)
    if 'gust' in MasterConfig.weather_data['wind'].keys():
        text = f'Gusts reaching {MasterConfig.weather_data["wind"]["gust"]} miles per hour.'
        speak(text, 150)
    # read out the forecast data
    forecast_analysis(MasterConfig.weather_data, MasterConfig.forecast)


def hour_conversion(timestamp):
    """Takes a unix timestamp and gets an hour and suffix"""
    hour = hour = int(datetime.fromtimestamp(timestamp).strftime("%H"))
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
    return (hour, sufix)


def forecast_analysis(current_data, forecast_data):
    """Analyze the forecast"""
    # https://openweathermap.org/weather-conditions
    # looking for key words 'rain' 'storm' 'drizzle' in the description
    # or id [200-232][300-321][500-531]
    # 711 - 781 excluding 721,741 are more sever weather conditions
    is_raining = False
    current_state = int(current_data['weather'][0]['id'])
    if current_state < 799:
        is_raining = True
    if is_raining:
        clear_found = False
        for i in range(0, 13, 1):
            if int(forecast_data['hourly'][i]['weather'][0]['id']) > 799:
                ts = forecast_data['hourly'][i]['dt']
                hour, sufix = hour_conversion(ts)
                clear_found = True
                break
        if clear_found:
            text = f'The rain should end around {hour}{sufix}'
            speak(text, 150)
        else:
            speak('It will rain for the next 12 hours.', 150)
    else:
        rain_found = False
        for i in range(1, 13, 1):
            if int(forecast_data['hourly'][i]['weather'][0]['id']) < 800:
                ts = forecast_data['hourly'][i]['dt']
                hour, sufix = hour_conversion(ts)
                rain_found = True
                break
        if rain_found:
            text = f'There is rain coming at {hour}{sufix}'
            speak(text, 150)
        else:
            speak('There is no approaching rain in the forecast.', 150)


def show_radar(browser):
    """Open the radar page in chrome"""
    def x():
        city = MasterConfig.current_city
        if not city:
            city = 'Atlanta'
        url = f'https://www.accuweather.com/en/us/{city}/28115/weather-radar/339828'
        return browser.open_new_tab(url)
    t = threading.Thread(target=x)
    t.start()
    city = MasterConfig.current_city
    if not city:
        city = 'Atlanta'
    text = f"Here's the radar for {city}"
    speak(text)


def write_note():
    """Writes a not to a text file in the jarvis folder"""
    speak('What would you like to write down?')
    note = listen().lower()
    # jarvis will append to the note pad
    date = datetime.now().strftime("%m/%d/%Y")
    with open('voice_notes\\notes.txt', 'a') as file:
        file.write(f'\n\n{date} - {note}')
    speak('Note written.')


def launch_weather_peripheral():
    """Launcher for the weather peripheral"""
    if 'weather_process' in MasterConfig.process_list.keys():
        try:
            os.kill(
                MasterConfig.process_list['weather_process'], signal.SIGTERM)
        except PermissionError as e:
            # kill will permission error if process is not existent
            # in this case we have what we want so just pass
            pass

    process = subprocess.Popen(['python', 'weather_peripheral.py'],
                               creationflags=subprocess.CREATE_NEW_CONSOLE, shell=False)
    return process.pid


def launch_stock_news_peripheral():
    """Launcher for the stock news peripheral"""
    if 'news_process' in MasterConfig.process_list.keys():
        try:
            os.kill(
                MasterConfig.process_list['news_process'], signal.SIGTERM)
        except PermissionError as e:
            # kill will permission error if process is not existent
            # in this case we have what we want so just pass
            pass

    process = subprocess.Popen(['python', 'stock_news_peripheral.py'],
                               creationflags=subprocess.CREATE_NEW_CONSOLE, shell=False)
    return process.pid


def launch_crypto_news_peripheral():
    """Launcher for the crypto news peripheral"""
    if 'news_process' in MasterConfig.process_list.keys():
        try:
            os.kill(
                MasterConfig.process_list['crypto_news_process'], signal.SIGTERM)
        except (PermissionError, KeyError) as e:
            # kill will permission error if process is not existent
            # in this case we have what we want so just pass
            pass

    process = subprocess.Popen(['python', 'crypto_news_peripheral.py'],
                               creationflags=subprocess.CREATE_NEW_CONSOLE, shell=False)
    return process.pid


def launch_notes_peripheral():
    """Launcher for the notes peripheral"""
    if 'notes_process' in MasterConfig.process_list.keys():
        try:
            os.kill(
                MasterConfig.process_list['notes_process'], signal.SIGTERM)
        except PermissionError as e:
            # kill will permission error if process is not existent
            # in this case we have what we want so just pass
            pass

    process = subprocess.Popen(['python', 'notes_peripheral.py'],
                               creationflags=subprocess.CREATE_NEW_CONSOLE, shell=False)
    return process.pid


def end_processes():
    """End any peripheral processes. Use when endind script. Format is 'process_name': pid"""
    if MasterConfig.process_list.keys():
        for key in tqdm(MasterConfig.process_list.keys()):
            try:
                os.kill(MasterConfig.process_list[key], signal.SIGTERM)
            except ProcessLookupError:
                print('Failed to find process to kill.')
