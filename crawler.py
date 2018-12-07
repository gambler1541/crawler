import requests
import os
from bs4 import BeautifulSoup
from urllib import parse

file_path = 'data/episode_list.html'
url_episode_list = 'https://comic.naver.com/webtoon/list.nhn'
params = {
    'titleId': 703845,
}

if os.path.exists(file_path):
    html = open('data/episode_list.html','rt').read()

else:
    r = requests.get(url_episode_list, params)
    with open('data/episode_list.html', 'w') as f:
        f.write(r.text)



soup = BeautifulSoup(html, 'lxml')

h2_title = soup.select_one('div.detail > h2')
title = h2_title.contents[0].strip()
author = h2_title.contents[1].get_text(strip=True)
description = soup.select_one('div.detail > p').get_text(strip=True)

print(title)
print(author)
print(description)


table = soup.select_one('table.viewList')
tr_list = table.select('tr')

for index, tr in enumerate(tr_list[1:]):
    if tr.get('class'):
        continue

    url_thumbnail = tr.select_one('td:nth-of-type(1) img').get('src')
    url_detail = tr.select_one('td:nth-of-type(1) > a').get('href')
    query_string = parse.urlsplit(url_detail).query
    query_dict = parse.parse_qs(query_string)
    no = query_dict['no'][0]

    title = tr.select_one('td:nth-of-type(2) > a').get_text(strip=True)
    rating = tr.select_one('td:nth-of-type(3) strong').get_text(strip=True)
    created_date = tr.select_one('td:nth-of-type(4)').get_text(strip=True)



    print(url_thumbnail)
    print(title)
    print(rating)
    print(created_date)
    print(no)




