# 重构源码
# 导入需要的模块
from bs4 import BeautifulSoup
import requests
import csv
import re

# 传递湾区日报链接，初始化HTML内容，返回BeautifulSoup对象
def get_one_page(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    html = r.text
    soup = BeautifulSoup(html, 'lxml')
    return soup


# 数据清洗，返回每一期的文章信息列表，每篇文章包含期数、标题、链接、阅读时长、简评
def parse_one_page(soup):
    ul = soup.find('ul', attrs={'class': 'list-group'})
    results = ul.find_all('li')[0:5]

    article_list = []
    
    # 获得期数
    issue = soup.title.string.strip()[11:-7]
    
    # 遍历所有文章，找到并清洗关键数据
    for result in results:
        try:
            # 获取标题
            title = result.h2.string
            # 获取链接
            link = result.find('a', attrs={'rel': 'external'}).get('href')
            # 获取阅读时长
            read_time_temp = result.find('a', attrs={'rel': 'external'}).text.replace(' ', '').replace('\n', '')
            read_time_temp = str(read_time_temp)
            read_time = re.match('.*?·(.*)读完', read_time_temp, re.S).group(1)
            # 获取简评
            summary = result.find('p', attrs={'class': 'summary-text'}).getText().strip().replace('\n', '')[:-22]
        except:
            continue
        
        article = [issue, title, link, read_time, summary]
        article_list.append(article)
        
    return article_list

# 传递pre_issue、end_issue，获得其中每一期的文章，并返回所有文章列表
def get_all_article(pre_issue, end_issue):
    print('爬取所有文章:')
    all_articles = []
    
    for issue in range(pre_issue, end_issue+1):
        url = 'https://wanqu.co/issues/' + str(issue) + '/'
        soup = get_one_page(url)
        articles = parse_one_page(soup)
        for article in articles:
            all_articles.append(article)
        print(issue)
        
    return all_articles

# 返回特定阅读时长文章列表
def read_time_article(article_list, pre_time, end_time):
    print('筛选的文章:')
    articles = []
    for article in article_list:
        if int(article[3][:-2]) in [mins for mins in range(pre_time, end_time+1)]:
            articles.append(article)
            print(article[0])

    return articles  


# 把数据写入csv文件中
def write_to_csv(articles):
    with open('wanqudaily.csv', 'w', newline='', encoding='utf-8-sig',) as f:
        csv_output = csv.writer(f)
        csv_output.writerows(articles)


# 获得780-1280之间每一期的文章
all_articles = get_all_article(780,1280)
# 获得阅读时长在1-5分钟的文章
read_time_articles = read_time_article(all_articles, 1, 5)
read_time_articles.insert(0,['期数', '标题', '链接', '阅读时长', '简评'])
write_to_csv(read_time_articles)





