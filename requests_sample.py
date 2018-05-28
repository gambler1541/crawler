import requests

response = requests.get('https://comic.naver.com/webtoon/weekday.nhn')
print(response.status_code)
# HTTP GET요청으로 받아온 Content를 text데이터로 리턴
print(response.text)
# response.text에 해당하는 데이터를
# weekday.html 이라는 파일에 기록
# 다 기록 했으면 close()호출

f = open('weekday.html', 'wt')
f.write(response.text)
f.close()

d