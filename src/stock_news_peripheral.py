import json
import time
from tqdm import tqdm
import MasterConfig
from rich.console import Console

console = Console(theme=MasterConfig.custom_theme)

with open(f'data\\stock_news.txt', 'r') as file:
    lines = file.readlines()

for line in tqdm(lines):
    print(line)

with open(f'data\\market_analysis.json', 'r') as file:
    data = json.load(file)

console.print('[bold white]Stocks[/bold white]:')
print(f'Articles searched: {data["headline_count"]}')
console.print(f'Positive keyphrases found: [good]{data["poscount"]}[/good]')
print(f'Neutral keyphrases found: {data["neucount"]}')
console.print(f'Negative keyphrases found: [critical]{data["negcount"]}[/critical]')

time.sleep(10000)
