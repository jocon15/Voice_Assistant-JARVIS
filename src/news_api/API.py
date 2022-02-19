"""This file is the web api for stock news."""
import json
import MasterConfig
from news_api.keywords import *
from requests_html import HTMLSession


def get_stock_news():
    url = 'https://news.google.com/rss/search?q=DOW'
    s = HTMLSession()
    r = s.get(url)
    # print(r.text)
    # for title in r.html.find('title'):
    #     print(title.text)

    with open(f'{MasterConfig.cwd}\\data\\stock_news.txt', 'w') as file:
        for title in r.html.find('title'):
            file.write(title.text)
            file.write('\n')

    # open the data file and extract data
    with open(f'{MasterConfig.cwd}\\data\\stock_news.txt', 'r') as file:
        lines = file.readlines()

    # filter out any bs headlines
    for headline in lines:
        if 'team' in headline or 'volleyball' in headline:
            lines.pop(lines.index(headline))
    # keyword search
    poscount = neucount = negcount = 0
    for headline in lines:
        for word in pos_words:
            if word in headline.lower():
                poscount += 1
        for word in neu_words:
            if word in headline.lower():
                neucount += 1
        for word in neg_words:
            if word in headline.lower():
                negcount += 1
    MasterConfig.top_3_stock_headlines = [lines[1], lines[2], lines[3]]
    MasterConfig.stock_news_analysis = (poscount, neucount, negcount)
    data = {
        'headline_count': len(lines),
        'poscount': poscount,
        'neucount': neucount,
        'negcount': negcount
    }
    with open(f'{MasterConfig.cwd}\\data\\market_analysis.json', 'w')as file:
        json.dump(data, file, indent=4)

    # print(f'Positive count: {poscount}')
    # print(f'Neutral count: {neucount}')
    # print(f'Negative count: {negcount}')


def get_crypto_news():
    url = 'https://news.google.com/rss/search?q=crypto'
    s = HTMLSession()
    r = s.get(url)

    # any codec errors were fixed by adding encoding='utf-8' to the reading and writing

    with open(f'{MasterConfig.cwd}\\data\\crypto_news.txt', 'w', encoding='utf-8') as file:
        for title in r.html.find('title'):
            file.write(title.text)
            file.write('\n')

    # open the data file and extract data
    with open(f'{MasterConfig.cwd}\\data\\crypto_news.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # filter out any bs headlines
    # for headline in lines:
    #     if 'team' in headline or 'volleyball' in headline:
    #         lines.pop(lines.index(headline))
    # keyword search
    poscount = neucount = negcount = 0
    for headline in lines:
        for word in pos_words:
            if word in headline.lower():
                poscount += 1
        for word in neu_words:
            if word in headline.lower():
                neucount += 1
        for word in neg_words:
            if word in headline.lower():
                negcount += 1
    MasterConfig.top_3_crypto_headlines = [lines[1], lines[2], lines[3]]
    MasterConfig.crypto_news_analysis = (poscount, neucount, negcount)
    data = {
        'headline_count': len(lines),
        'poscount': poscount,
        'neucount': neucount,
        'negcount': negcount
    }
    with open(f'{MasterConfig.cwd}\\data\\crypto_analysis.json', 'w')as file:
        json.dump(data, file, indent=4)

    # print(f'Positive count: {poscount}')
    # print(f'Neutral count: {neucount}')
    # print(f'Negative count: {negcount}')


if __name__ == '__main__':
    MasterConfig.cwd = 'D:\\Stock_Trading\\Source_Code\\Control_Center'
    # get_stock_news()
    # analyze_news()
    get_crypto_news()
