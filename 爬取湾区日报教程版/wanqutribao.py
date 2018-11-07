# 导入需要的模块
from bs4 import BeautifulSoup
import requests
import csv
import re

# 使用BeautifulSoup解析html数据
url = 'https://wanqu.co/issues/1280/'
r = requests.get(url)
r.encoding = 'utf-8'
html = r.text
soup = BeautifulSoup(html, 'lxml')
# print(soup)

# 查找HTML元素
ul = soup.find('ul', attrs={'class': 'list-group'})
results = ul.find_all('li')[0:5]
# print(results)

articles = []
articles.append(['期数', '标题', '链接', '阅读时长', '简评'])

issue = 1280
# 遍历所有文章，找到并清洗关键数据
for result in results:
    # 获取标题
    title = result.h2.string
    # 获取链接
    link = result.find('a', attrs={'rel': 'external'}).get('href')
    # 获取阅读时长
    read_time_temp = soup.find('a', attrs={'rel': 'external'}).text.replace(' ', '').replace('\n', '')
    read_time_temp = str(read_time_temp)
    read_time = re.match('.*?·(.*)读完', read_time_temp, re.S).group(1)
    # 获取简评
    summary = result.find('p', attrs={'class': 'summary-text'}).getText().strip().replace('\n', '')[:-22]
    
    article = [issue, title, link, read_time, summary]
    articles.append(article)  

# 把数据写入csv文件中
with open('wanqudaily.csv', 'w', newline='', encoding='utf-8-sig',) as f:
        csv_output = csv.writer(f)
        csv_output.writerows(articles)


   
