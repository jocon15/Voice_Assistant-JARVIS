from rich.theme import Theme

# colors get defined here with their hex value
# #26ff26
colors = {
    "status red": "bold red",
    "status yellow": "bold yellow",
    "status green": "bold green",
    "money green": "green",
    "money red": "red",
}
# colors then get assigned to a shorter word here
custom_theme = Theme({
    "bold": "bold white",
    "critical": colors['status red'],
    "warning": colors['status yellow'],
    "good": colors['status green'],
    "mgreen": colors['money green'],
    "mred": colors['money red'],
})


cwd = ''

current_city = ''

market_data = {}

weather_data = {}

forecast = {}

top_3_stock_headlines = []

top_3_crypto_headlines = []

stock_news_analysis = (0, 0, 0)

crypto_news_analysis = (0, 0, 0)

process_list = {}
