import os
from urllib import parse

import requests
from bs4 import BeautifulSoup


class Episode:
    def __init__(self,webtoon_id,no,url_thumbnail,title,rating,created_date):
        self.webtoon_id = webtoon_id
        self.no = no
        self.url_thumbnail = url_thumbnail
        self.title = title
        self.rating = rating
        self.created_date = created_date

    @property
    def url(self):
        url = 'http://comic.naver.com/webtoon/detail.nhn?'
        params = {
            'titleId': self.webtoon_id,
            'no': self.no,
        }
        episode_url = url + parse.urlencode(params)

        return episode_url


def webtoon_crawler(webtoon_id):
    '''
    webtoon_id 를 입력받아서 웹툰 title, author, description을 넘겨주는 함수
    :param webtoon_id:
    :return:
    '''
    file_path = 'data/episode_list-{webtoon_id}.html'.format(webtoon_id=webtoon_id)
    url_episode_list = 'https://comic.naver.com/webtoon/list.nhn'
    params = {
        'titleId': webtoon_id,
    }

    if os.path.exists(file_path):
        html = open(file_path, 'rt').read()

    else:
        r = requests.get(url_episode_list, params)
        with open(file_path, 'w') as f:
            f.write(r.text)

    soup = BeautifulSoup(html, 'lxml')

    h2_title = soup.select_one('div.detail > h2')
    title = h2_title.contents[0].strip()
    author = h2_title.contents[1].get_text(strip=True)
    description = soup.select_one('div.detail > p').get_text(strip=True)


    info = dict()
    info['title'] = title
    info['author'] = author
    info['description'] = description

    return info

def episode_crawler(webtoon_id):
    """
    webtoon_id를 입력받아서 webtoon_id, title, no, created_date등의 정보를 가져오는 크롤러
    :param webtoon_id:
    :return:
    """
    file_path = 'data/episode_list-{webtoon_id}.html'.format(webtoon_id=webtoon_id)

    if os.path.exists(file_path):
        html = open(file_path, 'rt').read()


    soup = BeautifulSoup(html, 'lxml')
    table = soup.select_one('table.viewList')
    tr_list = table.select('tr')


    episode_lists = list()
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


        # 매 에피소드 크롤링한 결과를 Episode클래스의 new_episode 인스턴스로 생성
        new_episode = Episode(
            webtoon_id = webtoon_id,
            no = no,
            url_thumbnail = url_thumbnail,
            title = title,
            rating = rating,
            created_date = created_date,
        )
        episode_lists.append(new_episode)

    return episode_lists



class Webtoon:
    def __init__(self,webtoon_id):
        self.webtoon_id = webtoon_id
        info = webtoon_crawler(webtoon_id)
        self.title = info['title']
        self.author = info['author']
        self.description = info['description']
        self.episode_list = list()


    def update(self):
        '''
        update 함수를 실행하면 해당 웹툰ID에 따른 에피소드 정보들을 Episode 인스턴스로 저장
        :return:
        '''
        result = episode_crawler(self.webtoon_id)
        self.episode_list = result



if __name__ == '__main__':
    webtoon1 = Webtoon(703845)
    print(webtoon1.title)
    webtoon1.update()
    for episode in webtoon1.episode_list:
        print(episode.url)
        print(f'형태형바보 {episdoe.episode_url}')