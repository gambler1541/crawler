from bs4 import BeautifulSoup
html = open('data/weekday.html', 'rt').read()
soup = BeautifulSoup(html, 'lxml')

div_content = soup.find('div', id='content')
div_list_area = div_content.find('div', class_= 'list_area')
div_col_list = div_list_area.find_all('div', class_ = 'col')
for col in div_col_list:
    print(col)


a_list = soup.select('')