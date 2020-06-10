import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime


def news():

    r = requests.get('https://www.reuters.com/finance/markets')
    soup = BeautifulSoup(r.text, 'html.parser')

    cache = []
    res = []

    section = 'tab-markets-'
    for region in range(3):

        if region == 0:
            section_id = section + 'us'
            RegionNews = soup.find(id=section_id)
            cache.append(news_all(RegionNews.find(class_='module-content')))

        elif region == 1:
            section_id = section + 'emea'
            RegionNews = soup.find(id=section_id)
            cache.append(news_all(RegionNews.find(class_='module-content')))

        else:
            section_id = section + 'asia'
            RegionNews = soup.find(id=section_id)
            cache.append(news_all(RegionNews.find(class_='module-content')))

    for region in range(len(cache)):
        for single in range(len(cache[region])):
            res.append(cache[region][single])

    res = sorted(res, key=lambda k: k['time'], reverse=True)

    res_am = []
    res_12am = []
    res_pm = []
    res_12pm = []
    res_date = []

    for r in res:
        if ':' in r['time']:
            if 'am' in r['time'] and '12' in r['time']:
                res_12am.append(r)
            elif 'am' in r['time']:
                res_am.append(r)
            elif 'pm' in r['time'] and '12' in r['time']:
                res_12pm.append(r)
            elif 'pm' in r['time']:
                res_pm.append(r)

        else:
            res_date.append(r)

    res_am = sorted(res_am, key=lambda k: datetime.strptime(k['time'][:k['time'].index('am')], '%H:%M'), reverse=True)
    res_12am = sorted(res_12am, key=lambda k: datetime.strptime(k['time'][:k['time'].index('am')], '%H:%M'), reverse=True)
    res_pm = sorted(res_pm, key=lambda k: datetime.strptime(k['time'][:k['time'].index('pm')], '%H:%M'), reverse=True)
    res_12pm = sorted(res_12pm, key=lambda k: datetime.strptime(k['time'][:k['time'].index('pm')], '%H:%M'), reverse=True)

    res_ordered = res_pm + res_12pm + res_am + res_12am + res_date

    data = {'News': res_ordered}
    json_dump = json.dumps(data)
    return json_dump


def news_all(News):

    obj = []
    for title, description, time in zip(range(len(News.find_all('a'))),
                                        range(len(News.find_all('p'))),
                                        range(len(News.find_all('time')))):
        article = {}
        article['title'] = News.find_all('a')[title].text.strip()
        article['description'] = News.find_all('p')[description].text.strip()
        article['time'] = News.find_all('time')[time].text.strip()
        article['link'] = 'https://www.reuters.com/' + News.find_all('a')[title].get('href')
        obj.append(article)

    return obj


