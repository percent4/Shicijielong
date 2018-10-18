import re
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

urls = ['https://so.gushiwen.org/gushi/tangshi.aspx',
        'https://so.gushiwen.org/gushi/sanbai.aspx',
        'https://so.gushiwen.org/gushi/songsan.aspx',
        'https://so.gushiwen.org/gushi/songci.aspx'
        ]

poem_links = []
for url in urls:
    # 请求头部
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}
    req = requests.get(url, headers=headers)

    soup = BeautifulSoup(req.text, "lxml")
    content = soup.find_all('div', class_="sons")[0]
    links = content.find_all('a')

    for link in links:
        poem_links.append('https://so.gushiwen.org'+link['href'])

poem_list = []
def get_poem(url):
    #url = 'https://so.gushiwen.org/shiwenv_45c396367f59.aspx'
    # 请求头部
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, "lxml")
    poem = soup.find('div', class_='contson').text.strip()
    poem = poem.replace(' ', '')
    poem = re.sub(re.compile(r"\([\s\S]*?\)"), '', poem)
    poem = re.sub(re.compile(r"（[\s\S]*?）"), '', poem)
    poem = re.sub(re.compile(r"。\([\s\S]*?）"), '', poem)
    poem = poem.replace('!', '！').replace('?', '？')
    poem_list.append(poem)

# 利用并发爬取
executor = ThreadPoolExecutor(max_workers=10)  # 可以自己调整max_workers,即线程的个数
# submit()的参数： 第一个为函数， 之后为该函数的传入参数，允许有多个
future_tasks = [executor.submit(get_poem, url) for url in poem_links]
# 等待所有的线程完成，才进入后续的执行
wait(future_tasks, return_when=ALL_COMPLETED)

# 将爬取的诗句写入txt文件
poems = list(set(poem_list))
poems = sorted(poems, key=lambda x:len(x))
for poem in poems:
    poem = poem.replace('《','').replace('》','') \
               .replace('：', '').replace('“', '')
    print(poem)
    with open('F://poem.txt', 'a') as f:
        f.write(poem)
        f.write('\n')

