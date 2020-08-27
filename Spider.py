#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import requests

req_num = 0
s = 0


def getall(purl):
    global s
    allpic_urls = []
    a = 5000
    t = 0
    print('Searching...')
    while t < a:
        url = purl + str(t)
        try:
            html = requests.get(url, timeout=8)
            t = t + 40
        except Exception:
            t = t + 40
            continue
        else:
            html.encoding = 'utf-8'
            content = html.text
            pic_urls = re.findall('"objURL":"(.*?)",', content, re.S)
            allpic_urls.extend(pic_urls)
            t = t + 40
    return allpic_urls


def download(allpic_urls, req, w):
    num = 0
    index = 0
    pd = os.path.exists(w)
    if pd == 0:
        os.makedirs(w)
    # pic_urls = re.findall('"objURL":"(.*?)",', content, re.S)
    while num < req:
        try:
            pic = requests.get(allpic_urls[index], timeout=5)
        except Exception as e:
            print(e)
            print(str(num) + r'/' + str(req_num) + ' fail ' + str(allpic_urls[index]))
            index += 1
            continue
        else:
            string = w + r'\\' + str(num+1) + '.jpg'
            f = open(string, 'wb')
            f.write(pic.content)
            f.close()
            print(str(num+1) + r'/' + str(req_num) + ' success ' + allpic_urls[index])
            #print(allpic_urls[index])
            num += 1
            index += 1


if __name__ == '__main__':
    word = input("请输入搜索内容： ")
    page_url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + word + '&pn='
    all_urls = getall(page_url)
    print("Sum of " + str(len(all_urls)))
    req_num = input("请输入下载数量：")
    print('Preparing...')
    download(all_urls, int(req_num), word)


