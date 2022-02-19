import base64
import keys

API_KEY = (base64.b64decode(keys.WEATHER_API_KEY)).decode('utf-8')
