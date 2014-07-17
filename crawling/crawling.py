# -*- coding:utf-8 -*-
import urllib2

def view_comic_title(page):
    response = urllib2.urlopen('http://comic.naver.com/webtoon/list.nhn?titleId=20853&weekday=tue'+'&page='+str(page))
    #print response.info()
    #html = response.read()
    #html = response.readlines()
    #print html

    html = response.read().split('<td class="title">')
    html = html[1:]
    for parts in html:
        print parts.split("</a>")[0].split(')">')[1]

for index in range(1,15):
    view_comic_title(index)
