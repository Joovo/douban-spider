 
from urllib import request
from urllib import error
from bs4 import BeautifulSoup
import chardet
import time
import re

ip_lists = []
domain = "http://www.xicidaili.com"

def get_iplists(target):
    try:
        # 构建请求
        req = request.Request(target)
        req.add_header("User-Agent","Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Mobile Safari/537.36")
        response = request.urlopen(req)
        html = response.read()

        # 用bs4解析
        soup = BeautifulSoup(html, 'lxml')

        # 提取我们需要的信息
        all_trs = soup.table.find_all('tr')[1:]

        # 这里只提取了IP:PORT
        for tr in all_trs:
            td = tr.find_all('td')
            ip_lists.append(td[1].string + ':' + td[2].string)

    except error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)

    # 尝试返回下一页的地址
    next_page = soup.find_all('a', class_='next_page')
    if next_page:
        next_url = next_page[0].get('href')
        return (domain + next_url)
    else:
        return None

def writeIP():
    if ip_lists:
        file = open("ip.txt", "w+", encoding="UTF-8")

        for ip in ip_lists:
            file.write(ip.strip() + '\n')

        file.close()

    else:
        print ("ip list is empty.")

if __name__ == "__main__":
    num = 500
    page = num // 100

    # 这里获取500个
    next_url = "http://www.xicidaili.com/nn"
    while (next_url is not None) and (page > 0):
        next_url = get_iplists(next_url)
        page = page - 1
        time.sleep(1)

    # 写入文件
    writeIP()