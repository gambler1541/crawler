import os
from urllib import parse
import requests
from bs4 import BeautifulSoup


class Episode:
    '''
    Episdoe 클래스는 Webtoon 클래스의 crawler_episode_list가 실행 될 때 생성됨

    '''
    def __init__(self, webtoon_id, no, url_thumbnail,title,rating,created_date):
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



    def get_image_url_list(self):
        file_path = 'data/episode_detail-{webtoon_id}-{episode_no}.html'.format(webtoon_id=self.webtoon_id, episode_no=self.no)
        if os.path.exists(file_path):
            html = open(file_path, 'rt').read()
        else:
            response = requests.get(self.url)
            html = response.text
            open(file_path, 'wt').write(html)


        soup = BeautifulSoup(html, 'lxml')
        img_list = soup.select('div.wt_viewer > img')
        return [img.get('src') for img in img_list]





class Webtoon:
    # Webtoon클래스는 webtoon_id만 초기인자로 받음
    def __init__(self, webtoon_id):
        self.webtoon_id = webtoon_id
        self._title = None
        self._author = None
        self._description = None
        self._episode_list = list()
        self._html = ''

    def _get_info(self, attr_name):
        '''
         속성이 없다면 set_info()함수 실행
        '''
        if not getattr(self, attr_name):
            self.set_info()
        return getattr(self, attr_name)

    # get_info를 통해 titiel, author,description을 가져옴
    @property
    def title(self):
        return self._get_info('_title')

    @property
    def author(self):
        return self._get_info('_author')

    @property
    def description(self):
        return self._get_info('_description')


    @property
    def html(self):
        '''

        data폴더에 episode_list파일이 있으면 파일을 열고, 없으면 생성 후
        request를 통해얻은 데이터를 html에 저장
        '''
        if not self._html:
            # data 폴더에 episode_list-{self.webtoonid}.html 파일이 있는지를 판단
            file_path = 'data/episode_list-{webtoon_id}.html'.format(webtoon_id=self.webtoon_id)
            url_episode_list = 'https://comic.naver.com/webtoon/list.nhn'
            params = {
                'titleId': self.webtoon_id,
            }

            if os.path.exists(file_path):
                # 만약 변수 file_path에 해당하는 파일이 있을 경우
                #
                # 해당 파일 오픈
                html = open(file_path, 'rt').read()

            else:
                # file_path에 해당하는 파일이 존재하지 않을 경우
                # url_episode_list에 해당하는 주소로 requests
                response = requests.get(url_episode_list, params)
                # requests한 자료를 html변수에 text로 할당
                html = response.text
                # 할당 후 file_path에 해당하는 파일을 생성, html에 저장한 데이터 덮어씀
                open(file_path, 'wt').write(html)
                # 해당 클래스의 html인스턴스에 html 할당
            self._html = html
            # 해당 클래스의 html 리턴
        return self._html

    def set_info(self):
        '''
        자신의 html속성을 파싱한 결과를 사용해
        자신의 title, author description속성값을 할당
        :return: None
        '''

        # 함수 html 의 리턴값인 self.html을 가지고 파싱
        # property로 만들었기 떄문에 속성처럼 사용가능
        soup = BeautifulSoup(self.html, 'lxml')
        # class명이 detail인 div의 자식속성 h2를 검색
        h2_title = soup.select_one('div.detail > h2')
        # h2_title에 해당하는 0번째 값인 제목을 title, 1번째 값인 작가를 author변수에 할당
        title = h2_title.contents[0].strip()
        author = h2_title.contents[1].get_text(strip=True)
        # class명이 detail인 div의 자식속성인 p태그를 찾고, p태그안에 있는 text를 가져옴
        description = soup.select_one('div.detail > p').get_text(strip=True)

        self._title = title
        self._author = author
        self._description = description

    def crawl_episode_list(self):
        """
        webtoon_id를 입력받아서 webtoon_id, title, no, created_date등의 정보를 가져오는 크롤러

        :return:
        """
        soup = BeautifulSoup(self.html, 'lxml')
        table = soup.select_one('table.viewList')
        tr_list = table.select('tr')

        episode_list = list()
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
                webtoon_id=self.webtoon_id,
                no=no,
                url_thumbnail=url_thumbnail,
                title=title,
                rating=rating,
                created_date=created_date,
            )
            episode_list.append(new_episode)

        self._episode_list = episode_list

    @property
    def episode_list(self):
        if not self._episode_list:
            self.crawl_episode_list()
        return self._episode_list



#
if __name__ == '__main__':
    webtoon1 = Webtoon(703845)
    e1 = webtoon1.episode_list
    print(e1.get_image_url_list(4))


